import os
import discord

from utils import load_credential
from audio_parser import AudioParser

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)
parser = AudioParser()

async def process_audio(file_path):
    print(f"Processing audio file: {file_path}")
    return parser.summarize_daily_log(file_path)

@client.event
async def on_message(message):
    # Only respond to DMs from users (not bots)
    if message.guild is None and not message.author.bot:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("audio"):
                file_name = f"audios/{attachment.filename}"
                os.makedirs("audios", exist_ok=True)
                await attachment.save(file_name)
                response = await process_audio(file_name)
                await message.channel.send(response)
                break

if __name__ == "__main__":
    if not load_credential("bot_token"):
        raise ValueError("Bot token is missing.")
    if not load_credential("gemini_api_key"):
        raise ValueError("Gemini API key is missing.")

    print("Starting Discord bot...")
    client.run(load_credential("bot_token"))