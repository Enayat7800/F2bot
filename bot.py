from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Telegram API credentials
api_id = os.getenv('API_ID')  # Telegram se API ID le aao
api_hash = os.getenv('API_HASH')  # Telegram se API Hash le aao
bot_token = os.getenv('BOT_TOKEN')  # BotFather se bot token le aao

# Your channel ID
your_channel_id = None

# List to store multiple channels
source_channels = []

# Client setup
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Command: /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Hello bhai! Main tumhara bot hu. Mujhe use karne ke liye commands try karo. 😄")

# Command: /help
@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.reply("Commands list:\n"
                      "/start - Bot ko start karo\n"
                      "/help - Help message dikhao\n"
                      "/mychannel - Apne channel ka ID set karo\n"
                      "/addchannel - Naya channel add karo\n"
                      "/listchannels - Added channels ki list dikhao\n"
                      "/copy - Added channels se messages copy karo")

# Command: /mychannel
@client.on(events.NewMessage(pattern='/mychannel'))
async def set_my_channel(event):
    global your_channel_id
    try:
        your_channel_id = int(event.message.text.split(' ')[1])  # Command ke baad ka text extract karo
        await event.reply(f"Apna channel ID `{your_channel_id}` set ho gaya hai! ✅")
    except (IndexError, ValueError):
        await event.reply("Sahi format mein channel ID daalo. Example: `/mychannel -1001234567890`")

# Command: /addchannel
@client.on(events.NewMessage(pattern='/addchannel'))
async def add_channel(event):
    try:
        channel_input = event.message.text.split(' ')[1]  # Command ke baad ka text extract karo
        if channel_input not in source_channels:
            source_channels.append(channel_input)
            await event.reply(f"Channel `{channel_input}` successfully added! ✅")
        else:
            await event.reply(f"Channel `{channel_input}` already exists in the list.")
    except IndexError:
        await event.reply("Sahi format mein channel ID ya username daalo. Example: `/addchannel @channel_username` ya `/addchannel -1001234567890`")

# Command: /listchannels
@client.on(events.NewMessage(pattern='/listchannels'))
async def list_channels(event):
    if source_channels:
        channels_list = "\n".join(source_channels)
        await event.reply(f"Added channels:\n{channels_list}")
    else:
        await event.reply("No channels added yet. Use `/addchannel` to add a channel.")

# Command: /copy
@client.on(events.NewMessage(pattern='/copy'))
async def copy(event):
    if not your_channel_id:
        await event.reply("Pehle apna channel ID set karo `/mychannel` command se.")
        return

    if not source_channels:
        await event.reply("Pehle kuch channels add karo `/addchannel` command se.")
        return

    for channel_input in source_channels:
        try:
            messages = await client.get_messages(channel_input, limit=10)  # Last 10 messages fetch karo
            for message in messages:
                await client.send_message(your_channel_id, message.text)
            await event.reply(f"Messages from `{channel_input}` successfully copied! ✅")
        except Exception as e:
            await event.reply(f"Error copying messages from `{channel_input}`: {str(e)}")

# Bot ko start karo
print("Bot is running...")
client.run_until_disconnected()
