import aiohttp
import asyncio
import json
from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class File:
    content: str
    filename: str = ""


@dataclass
class RunStage:
    stdout: str
    stderr: str
    output: str
    code: int
    signal: Any


class Output:
    def __init__(self, json_response: dict):
        self.raw_json = json_response
        self.language = json_response.get("language")
        self.version = json_response.get("version")
        self.run_stage = None

        runstage = json_response.get("run")
        if runstage:
            self.run_stage = RunStage(
                stdout=runstage.get("stdout"),
                stderr=runstage.get("stderr"),
                output=runstage.get("output"),
                code=runstage.get("code"),
                signal=runstage.get("signal"),
            )

    def __repr__(self):
        return f"{self.language} {self.version} {self.run_stage.output}"

    def __str__(self):
        return self.run_stage.output


class CodeRunner:
    BASE_URL = "https://emkc.org/api/v2/piston/"
    
    def __init__(self, api_key: Optional[str] = None):
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": "Custom Piston Client"
        }
        if api_key:
            self._headers["Authorization"] = api_key
        
    async def execute(
        self,
        language: str,
        files: List[File],
        version: str = "*",
        stdin: str = "",
        args: list = [],
        compile_timeout: int = 10000,
        run_timeout: int = 3000,
        compile_memory_limit: int = -1,
        run_memory_limit: int = -1,
    ) -> Output:
        """Выполняет код через API Piston"""
        
        payload = {
            "language": language,
            "version": version,
            "stdin": stdin,
            "args": args,
            "compile_timeout": compile_timeout,
            "run_timeout": run_timeout,
            "compile_memory_limit": compile_memory_limit,
            "run_memory_limit": run_memory_limit,
        }
        
        files_json = []
        for file in files:
            files_json.append({"name": file.filename, "content": file.content})
        
        payload["files"] = files_json
        
        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.post(
                f"{self.BASE_URL}execute/", 
                data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return Output(result)
                else:
                    error_text = await response.text()
                    raise Exception(f"API вернула ошибку: {response.status} - {error_text}")
