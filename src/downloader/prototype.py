import aiohttp
from abc import ABC, abstractmethod
from http.cookies import SimpleCookie


############################# GENERIC CLASS #############################
class GenericWebsite(ABC):
    def __init__(self) -> None:
        self.attempts: int = 2
        self.threshhold: int = 3
        self.base_url: str = None
        self.search_url: str = None
        self.params: dict = None
        self.cookies: SimpleCookie = None
        self.headers: dict = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
        
        
    @abstractmethod
    async def get_cookies(self) -> SimpleCookie:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.base_url) as response:
                self.cookies = response.cookies
    
    @abstractmethod
    async def get_song(self) -> None:
        pass
    
    @abstractmethod
    async def get_page(self, url:str=None, title:str=None, only_url:bool=False) -> str:
        if title:
            self.params[list(self.params)[0]] = title
            params: dict = self.params
        else:
            params = None
        
        for _ in range(self.attempts):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url or self.search_url, params=params, cookies=self.cookies, headers=self.headers, allow_redirects=True) as response:
                    if response.status == 200:
                        if only_url:
                            page = None
                        elif not only_url:
                            page: str = await response.text()
                        return page, response.url
                    else:
                        await self.get_cookies()
    
    @abstractmethod
    async def run(self, title: str) -> list[str]:
        if not self.cookies:
            await self.get_cookies()
            
        page, _ = await self.get_page(title)
        download_url: list[str] = await self.get_song(page, title)
        return download_url