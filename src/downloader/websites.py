import asyncio
import base64
from bs4 import BeautifulSoup
from bs4.element import Tag
from http.cookies import SimpleCookie
from src.downloader.prototype import GenericWebsite
import re


################################## Z3fm #################################
class Z3fm(GenericWebsite):
    def __init__(self) -> None:
        super().__init__()
        
        self.base_url: str = "https://z3.fm/"
        self.search_url: str = "https://z3.fm/mp3/search"
        self.params: dict = {'keywords': None}
        self.cookies: SimpleCookie = None
        
    async def get_cookies(self) -> SimpleCookie:
        await super().get_cookies()
    
    
    async def get_page(self, title: str) -> str:
        return await super().get_page(title=title)
    
    
    async def get_song(self, page: str, title: str) -> list[str]:
        soup = BeautifulSoup(page, "html.parser")
        # Locate the download-url
        tags_download: Tag = soup.find("div", {'class': 'whb_box'}).find_all("span", {'class': 'song-download btn4 download'})[:self.threshhold]
        
        try:
            # Locate downloading URL
            download_urls: list[str] = [f'{self.base_url}{x["data-url"]}' for x in tags_download]
        except TypeError:
            return
        return download_urls
    
    
    async def run(self, title: str) -> str:
        return await super().run(title)


################################# SEFON #################################
class Sefon(GenericWebsite):
    def __init__(self) -> None:
        super().__init__()
        
        self.base_url: str = "https://sefon.pro/"
        self.search_url: str = "https://sefon.pro/search/"
        self.params: dict = {'q': None}
        self.cookies: SimpleCookie = None
        
    async def get_cookies(self) -> SimpleCookie:
        await super().get_cookies()
    
    
    async def get_page(self, title: str) -> str:
        return await super().get_page(title=title)
    
    
    async def parse(self, page: str) -> str:
        soup = BeautifulSoup(page, "html.parser")
        href: str = soup.find("div", class_="b_song_info").find("div", class_="btns").find("a", class_="b_btn download no-ajix url_protected")['href'][1:]
        data_key: str = soup.find("div", class_="b_song_info").find("div", class_="btns").find("a", class_="b_btn download no-ajix url_protected")['data-key']
        return href, data_key
    
    
    async def decode_url(self, href: str, data_key: str) -> str:
        for char in data_key[::-1]:
            href: str = char.join(reversed(href.split(char)))
            
        download_url: str = base64.b64decode(href).decode('utf-8')
        download_url: str = f'{self.base_url}{download_url[1:]}'
        return download_url
    
    
    async def process_url(self, url: str) -> str:
        page, _ = await super().get_page(url=f'{self.base_url}{url}')
        href, data_key = await self.parse(page)
        download_url: str = await self.decode_url(href, data_key)
        _, download_url = await super().get_page(url=download_url, only_url=True)
        return download_url
    
    
    
    async def get_song(self, page: str, title: str) -> list[str]:
        soup = BeautifulSoup(page, "html.parser")
        
        try:
            # Get the first items on the search list
            tags_download: Tag = soup.find_all("div", {"class": "song_name"})[:self.threshhold]
            # Locate downloading URL
            download_urls: list[str] = [x.find("a", {"href": True})['href'][1:] for x in tags_download]
            
            tasks = [
                asyncio.create_task(self.process_url(url))
                for url in download_urls]
            download_urls: list = await asyncio.gather(*tasks)
            
        except TypeError:
            return
        
        return download_urls
    
    
    async def run(self, title: str) -> str:
        return await super().run(title)


################################# MINTY #################################
class Minty(GenericWebsite):
    def __init__(self) -> None:
        super().__init__()
        
        self.base_url: str = "https://minty.club/"
        self.search_url: str = "https://minty.club/search"
        self.params: dict = {'q': None}
        self.cookies: SimpleCookie = None
        
    async def get_cookies(self) -> SimpleCookie:
        await super().get_cookies()
        
        
    async def get_page(self, title: str) -> str:
        return await super().get_page(title=title)
    
    
    async def parse(self, item: Tag, title: str) -> str:
        song_creds: str = re.sub('\W+', ' ', item.find("a", class_="track-row__description").text).strip()
        if set(title.lower().split()).issubset(song_creds.lower().split()):
            download_url: str = item.find("a", class_="track-row__download", href=True)["href"]
            download_url: str = f'{self.base_url[:-1]}{download_url}'
            return download_url
        else: return
    
    
    async def get_song(self, page: str, title: str) -> list[str]:
        soup = BeautifulSoup(page, "html.parser")
        
        try:
            
            content: list[Tag] = soup.find_all("div", class_="track-row__wrapper")[:self.threshhold]
            
            tasks = [asyncio.create_task(self.parse(item, title)) for item in content]
            download_urls: list[str] = await asyncio.gather(*tasks)
            return download_urls
            
        except Exception:
            return
        
        
    async def run(self, title: str) -> str:
        return await super().run(title)