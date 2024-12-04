import asyncio
from typing import Union
from pyrogram import Client
from pyrogram.errors import FloodWait

async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    """
    Create a chat invite link, with handling for FloodWait exceptions.
    """
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"FloodWait: Sleeping for {e.value} seconds...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)
