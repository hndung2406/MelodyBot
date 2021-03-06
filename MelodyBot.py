# token NTM3NDcwOTMyNDIwMjYzOTU4.DylumQ.wPV5QVD_mPYAiRQucfBYaYHSHZ4
# id 537470932420263958
# permission 67648
# https://discordapp.com/oauth2/authorize?client_id=537470932420263958&scope=bot&permissions=67648
import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import youtube_dl

TOKEN = "NTM3NDcwOTMyNDIwMjYzOTU4.DylumQ.wPV5QVD_mPYAiRQucfBYaYHSHZ4"
client = commands.Bot(command_prefix='!')
client.remove_command('help')
status = ['Dota 2', 'Artifact', 'Hearthstone']

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


def report_guild(guild):
    online = 0
    offline = 0
    idle = 0
    for member in guild.members:
        if str(member.status) == "online":
            online += 1
        elif str(member.status) == "offline":
            offline += 1
        else:
            idle += 1
    return online, offline, idle


@client.event  # event decorator/wrapper
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='Dota 2'))
    print(f"We have login {client.user}")


@client.event
async def on_message(message):
    global melody_guild
    melody_guild = client.get_guild(537469047634395156)
    print('An user has sent a message')
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Minions')
    await member.add_roles(role)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name='Help')
    embed.add_field(name='!exit', value='Exit the program', inline=False)
    embed.add_field(name='!report', value='Report the status of member in guild', inline=False)
    embed.add_field(name='!repeat', value='Repeat what you have just entered', inline=False)
    embed.add_field(name='!count', value='Count the number of member in the guild', inline=False)
    embed.add_field(name='!clear', value='Clear the channel', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def exit(ctx):
    await ctx.send(f'```Peace!!!```')
    await client.close()


@client.command()
async def count(ctx):
    await ctx.send(f"```py\nTotal member: {melody_guild.member_count}```")


@client.command()
async def report(ctx):
    online, offline, idle = report_guild(melody_guild)
    await ctx.send(f'```py\nOnline: {online}\nOffline: {offline}\nIdle: {idle}```')


@client.command()
async def repeat(ctx, *args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.send(output)


@client.command()
async def clear(ctx):
    channel = ctx.message.channel
    messages = await channel.history().flatten()
    await channel.delete_messages(messages)


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()


@client.command()
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()


@client.command()
async def play(ctx, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))


@client.command()
async def stream(ctx, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))


# Change the status of the bot every 5 mins
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)
    while not client.is_closed():
        current_status = next(msgs)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=current_status))
        await asyncio.sleep(300)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client.loop.create_task(change_status())
client.run(TOKEN)
