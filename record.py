import discord
import discord.opus
import asyncio
from discord.ext import commands
from utils import load_credential

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
# Keep track of recording state manually
recording_state = {}
bot.voice_connections = {}  # dictionary guild_id -> vc


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def record(ctx):
    """Join your VC if not already there, then start recording until !stop is called."""
    if not ctx.author.voice:
        await ctx.send("❌ You must be in a voice channel to start recording.")
        return

    vc: discord.VoiceClient = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
        await ctx.send(f"🔊 Joined {ctx.author.voice.channel.name}")

    # Check our manual state
    if recording_state.get(ctx.guild.id, False):
        await ctx.send("⚠️ Already recording in this server!")
        return

    # Ensure we're properly connected before trying to record
    if not vc.is_connected():
        await ctx.send("❌ Failed to connect to voice channel. Please try again.")
        return

    sink = discord.sinks.WaveSink()

    def finished_callback(sink, *args):
        for user_id, audio in sink.audio_data.items():
            user = bot.get_user(user_id)
            filename = f"{user.name}_{user_id}.wav"
            with open(filename, "wb") as f:
                f.write(audio.file.read())
            print(f"💾 Saved recording for {user} -> {filename}")
        # Reset state when done
        recording_state[ctx.guild.id] = False

    await asyncio.sleep(0.3)
    vc.start_recording(sink, finished_callback, ctx.channel)

    recording_state[ctx.guild.id] = True
    await ctx.send("🎙️ Started recording! Use `!stop` to finish.")


@bot.command()
async def stop(ctx):
    """Stop the current recording (but stay in channel)."""
    vc: discord.VoiceClient = ctx.voice_client
    if not vc or not recording_state.get(ctx.guild.id, False):
        await ctx.send("❌ Not currently recording.")
        return

    await vc.stop_recording()  # will trigger callback
    await ctx.send("✅ Recording stopped! Files saved.")


@bot.command()
async def join(ctx):
    """Join the voice channel of the command issuer."""
    if not ctx.author.voice:
        await ctx.send("❌ You must be in a voice channel to summon me.")
        return

    vc: discord.VoiceClient = ctx.voice_client
    if vc and vc.is_connected():
        await ctx.send("⚠️ I'm already in a voice channel!")
        return

    vc = await ctx.author.voice.channel.connect(timeout=120, reconnect=True)
    print(f"🔊 Joined {ctx.author.voice.channel.name}")
    bot.voice_connections[ctx.guild.id] = vc  # keep reference alive


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the channel.")


bot.run(load_credential())
