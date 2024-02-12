import aiohttp
import asyncio
import itertools
from src.downloader.websites import Z3fm, Sefon, Minty


class Downloader:
    def __init__(self):
        self.z3fm: Z3fm = None
        self.sefon: Sefon = None
        self.minty: Minty = None
        
    async def run(self, title: str) -> list[str]:
        if any(website is None for website in [self.z3fm, self.sefon, self.minty]):
            self.z3fm = Z3fm()
            self.sefon = Sefon()
            self.minty = Minty()
        
        workers = [
            asyncio.create_task(self.z3fm.run(title)),
            asyncio.create_task(self.sefon.run(title)),
            asyncio.create_task(self.minty.run(title))]
        
        done, _ = await asyncio.wait(workers)
        songs = [task.result() for task in done if task.result()]
        songs: list[str] = list(itertools.chain(*songs))
        songs: list[str] = [x for x in songs if x]
        return songs