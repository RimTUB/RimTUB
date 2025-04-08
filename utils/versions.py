import aiohttp
from utils import Config

async def get_available_module_versions(module_name, module_version):
    
    URL = Config.CHECK_VERSIONS_URL.format(module_name=module_name, module_version=module_version)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                data = await response.json()
                 
                if data:
                    return data['available_RimTUB_versions']
    except:
        return None