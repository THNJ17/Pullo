import os
import discord
from discord.ext import commands
import asyncio
import youtube_dl

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True
# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Create a dictionary to store the voice clients for each guild
voice_clients = {}

# Define the options for ytdl
ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(id)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}

# Create a ytdl object with the options
ytdl = youtube_dl.YoutubeDL(ytdl_opts)

# Define the options for FFmpegc
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Add a command to play music
@bot.command()
async def play(ctx, *args):
    # Get the voice client for the guild
    voice_client = ctx.voice_client

    # Check if the bot is already connected to a voice channel
    if not voice_client:
        # Get the user's voice channel
        voice_channel = ctx.author.voice.channel

        # Connect to the voice channel
        voice_client = await voice_channel.connect()
        voice_clients[ctx.guild.id] = voice_client

    # Loop through the arguments to get the URLs
    for url in args:
        # Extract the info for the video
        info = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        # Get the audio stream
        audio_stream = discord.FFmpegPCMAudio(info['url'], **ffmpeg_options)

        # Add the audio stream to the queue
        voice_client.play(audio_stream)

    # Send a message to the user
    await ctx.send('Playing ',  )

# Add a command to pause the music
@bot.command()
async def pause(ctx):
    # Get the voice client for the guild
    voice_client = ctx.voice_client

    # Pause the music
    voice_client.pause()

    # Send a message to the user
    await ctx.send('Music paused.')

# Add a command to resume the music
@bot.command()
async def resume(ctx):
    # Get the voice client for the guild
    voice_client = ctx.voice_client

    # Resume the music
    voice_client.resume()

    # Send a message to the user
    await ctx.send('Music resumed.')

# Add a command to stop the music and disconnect from the voice channel
@bot.command()
async def disconnect(ctx):
    # Check if the bot is connected to a voice channel
    voice_client = ctx.voice_client
    if voice_client:
        # Stop playing and disconnect from the voice channel
        await voice_client.disconnect()
        await ctx.send("Okay, disconnecting :(")
    else:
        await ctx.send('I am not connected to a voice channel')

# Run the bot
bot.run('insert discord token here')
