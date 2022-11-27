import discord
import logging
import re
from typing import Iterable, Callable, Optional

from google_image import GoogleImage

def try_generator(_iter: Iterable, pipeline: Optional[Callable]=None) -> Iterable:
    pipeline = pipeline or (lambda x: x)
    for i in _iter:
        try:
            yield pipeline(i)
        except Exception:
            pass
        except RuntimeError as e:
            raise e

class JPEGBot(discord.Client):
    async def on_ready(self) -> None:
        logging.info('client ready')
        logging.info(f'logged as {self.user}')

    async def on_message(self, message: str) -> None:
        if message.author == self.user:
            return
        if (match := re.match(r'([^\s\.]+)\.jpg', message.content)):
            keyword = match.group(1)
            _images = GoogleImage(keyword.replace('_', ' ')).target_images
            _images_generator = try_generator(_images, lambda img: img.buffer)
            _buffer = next(_images_generator)

            if _buffer:
                await message.channel.send(file=discord.File(_buffer, filename=f"{keyword}.jpg"))
            else:
                await message.channel.send(text="找不到QQ")

            # try:
            #     _images_generator.close()
            # except Exception:
            #     pass
