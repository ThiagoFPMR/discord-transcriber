import yaml
import discord
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="hello")
async def hello(interaction):
    await interaction.response.send_message("Hello!", ephemeral=True)


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    bot.run(config["token"])
