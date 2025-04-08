import gzip
from pathlib import Path
import shutil
import aiohttp
import asyncio
import json
import os
from utils.exceptions import ModuleError
from utils.scripts import try_



def tgs_to_json(tgs_path: Path, json_path):
    if not tgs_path.suffix.lower() == '.tgs':
        raise ValueError(f"Invalid file type: {tgs_path} (Expected .tgs file)")

    with gzip.open(tgs_path, 'rb') as f_in:
        with open(json_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    
    return json_path

async def upload_lottie_json(session: aiohttp.ClientSession, json_data):
    url = 'https://html5animationtogif.com/api/uploadlottiejsonfile.ashx'
    data = {
        'file': json_data
    }
    
    async with session.post(url, data=data) as response:
        response_data = json.loads(await response.text())
        if response_data['status'] == 'success':
            return response_data['creativeid']
        else:
            raise ModuleError(f"Error: {response_data['message']}")
            return None

async def convert_lottie_to_gif(session, creative_id, width, height, duration, fps, webhook_url="", api_data=None):
    url = 'https://html5animationtogif.com/api/convertlottietogif.ashx'
    data = {
        'clientid': api_data['client_id'],
        'apikey': api_data['api_key'],
        'creativeid': creative_id,
        'width': width,
        'height': height,
        'duration': duration,
        'fps': fps,
        'webhookurl': webhook_url,
        'transparency': "Y"
    }
    
    async with session.post(url, data=data) as response:
        response_data = json.loads(await response.text())
        if response_data['status'] == 'success':
            return response_data['mediaid']
        else:
            raise ModuleError(f"Error: {response_data['message']}")
            return None

async def check_conversion_status(session, creative_id, media_id, loading):
    url = 'https://html5animationtogif.com/api/checkstatus.ashx'
    params = {
        'creativeid': creative_id,
        'mediaid': media_id,
        'fileext': 'gif'
    }
    
    async with session.get(url, params=params) as response:
        response_data = json.loads(await response.text())
        if loading:
            if '%' in (s:=response_data['jobstatus']):
                await loading(None, int(s.replace('%', '')), None)
            else:
                await loading(response_data['jobstatus'], None, None)
            
        if response_data['status'] == 'success':
            if response_data['jobstatus'] == 'done':
                return response_data['url']
            else:
                return None
        else:
            if loading:
                await loading('error', int(s.replace('%', 0)), response_data['message'])
            raise ModuleError(f"Error: {response_data['message']}")
            return None

async def download_gif(session, download_url, save_path):
    async with session.get(download_url) as response:
        with open(save_path, 'wb') as f:
            f.write(await response.read())

async def process_tgs_file(
    tgs_path, json_path, out_gif_path,
    width=512*2, height=512, duration=3, fps=60,
    webhook_url="", update_delay=10, loading=None,
    api_data=None):
    async with aiohttp.ClientSession() as session:
        json_path = tgs_to_json(tgs_path, json_path)
        
        with open(json_path, 'rb') as f:
            creative_id = await upload_lottie_json(session, f)
        
        if creative_id:
            media_id = await convert_lottie_to_gif(session, creative_id, width, height, duration, fps, webhook_url, api_data)
            
            if media_id:
                download_url = None
                while not download_url:
                    download_url = await check_conversion_status(session, creative_id, media_id, loading)
                    if not download_url:
                        await asyncio.sleep(update_delay)
                
                await download_gif(session, download_url, out_gif_path)


from PIL import Image, ImageSequence

def crop_gif_to_square(gif_path, out_path):
    img = Image.open(gif_path)

    w, h = img.size
    side = min(w, h)

    left = (w - side) // 2
    top = (h - side) // 2
    right = left + side
    bottom = top + side

    frames = []
    durations = []
    disposals = []

    for frame in ImageSequence.Iterator(img):
        cropped_frame = frame.crop((left, top, right, bottom)).convert("RGBA")
        frames.append(cropped_frame)
        durations.append(frame.info.get("duration", 100))
        disposals.append(frame.info.get("disposal", 2)) 


    frames[0].save(out_path, save_all=True, append_images=frames[1:], loop=0, duration=durations, disposal=2)

    return out_path


async def convert(path, out_path, loading, api_data):
    
    path = Path(path)
    
    watermarked_path = path.with_stem(path.stem + "_watermarked").with_suffix(".gif")
    json_path = path.with_suffix(".json")
    
    await process_tgs_file(path, json_path, watermarked_path, 512*2, 512, 3, 30, update_delay=3, loading=loading, api_data=api_data)
 
    crop_gif_to_square(watermarked_path, out_path)
    
    try_(os.remove(path))
    try_(os.remove(watermarked_path))
    try_(os.remove(json_path))
    
    return out_path
    
