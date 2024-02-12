import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext


class SendingQueue:
    def __init__(self, commandHandler, media: list[str], callback_query: types.Message, state: FSMContext) -> None:
        self.threshold: int = 2 # limit is up to 10
        self.callback_query: types.Message = callback_query
        self.handler = commandHandler
        self.media: list[str] = media
        self.queue = asyncio.Queue()
        self.state: FSMContext = state
    
    
    async def fill_queue(self):
        for item in self.media:
            self.queue.put_nowait(item)
    
    async def run(self):
        # Add items into the queue
        await self.fill_queue()
        # Start the queue loop
        while not self.queue.empty():
            attachments: list[str] = []
            # If less items left in the queue then a set threshold
            if self.queue.qsize() / self.threshold < 1:
                self.threshold = self.queue.qsize()
            # Get items from queue. Send to telegram
            if self.queue.qsize() >= self.threshold:
                while len(attachments) != self.threshold:
                    attachments.append(self.queue.get_nowait())
                await self.handler.send_songs(self.callback_query, attachments, self.state)
                attachments.clear()
                
                if self.queue.qsize() >= 1:
                    # Send a captcha
                    answer: bool = await self.handler.captcha(self.callback_query, self.queue.qsize())
                    if not answer:
                        break