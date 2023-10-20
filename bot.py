import discord
import json
import os

token = os.environ["BOT_TOKEN"]
intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    for guild in client.guilds:
        print(f"Dumping guild {guild.name}")
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                print(f"Dumping channel {channel.name}")
                await dump_channel(guild.name, channel)


async def dump_channel(guild_name: str, channel: discord.TextChannel):
    messages = []
    async for message in channel.history(limit=None, oldest_first=True):
        try:
            if message.author.bot:
                continue
            message_dict = {
                "id": message.id,
                "author": message.author.name,
                "content": message.clean_content,
                "created_at": message.created_at.timestamp(),
                "attachments": [
                    {"filename": i.filename, "url": i.url} for i in message.attachments
                ],
                "reply_to": message.reference.message_id
                if message.type == discord.MessageType.reply and message.reference
                else None,
            }
            messages.append(message_dict)
            if len(messages) % 1000 == 0:
                print(len(messages))
                print(message_dict)
        except Exception as e:
            print(e)
            continue
    dir_path = f"dumps/{guild_name}"
    os.makedirs(dir_path, exist_ok=True)
    with open(f"{dir_path}/{channel.name}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(messages, indent=2, ensure_ascii=False))


client.run(token)
