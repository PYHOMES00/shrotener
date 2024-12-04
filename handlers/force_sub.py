from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from configs import Config
from invite_link import get_invite_link

async def handle_force_sub(bot: Client, cmd: Message):
    """
    Enforce subscription to three channels before using the bot.
    """
    channels = [
        Config.UPDATES_CHANNEL_1,
        Config.UPDATES_CHANNEL_2,
        Config.UPDATES_CHANNEL_3,
    ]
    missing_channels = []

    for channel in channels:
        if channel.startswith("-100"):
            chat_id = int(channel)
        else:
            chat_id = channel

        try:
            user = await bot.get_chat_member(chat_id=chat_id, user_id=cmd.from_user.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text=f"Sorry Sir, you are banned from using this bot. "
                         f"[Contact Support](https://t.me/ur_HemtaiZ_Bot).",
                    disable_web_page_preview=True
                )
                return 400
        except UserNotParticipant:
            missing_channels.append(chat_id)
        except Exception as err:
            print(f"Unexpected error for channel {channel}: {err}")
            return 200  # Allow access in case of unexpected issues.

    if missing_channels:
        await prompt_subscription(bot, cmd, missing_channels)
        return 400

    return 200  # User is subscribed to all channels.

async def prompt_subscription(bot: Client, cmd: Message, missing_channels: list):
    """
    Prompt the user to subscribe to missing channels.
    """
    buttons = []
    for channel_id in missing_channels:
        try:
            invite_link = await get_invite_link(bot, chat_id=channel_id)
            buttons.append([InlineKeyboardButton("Join Channel", url=invite_link.invite_link)])
        except Exception as err:
            print(f"Failed to generate invite link for {channel_id}. Error: {err}")
            continue

    if buttons:
        buttons.append([InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshForceSub")])
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please join the following channels to use this bot:**\n\n"
                 "Due to overload, only subscribers can access the bot.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
