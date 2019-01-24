# token NTM3NDcwOTMyNDIwMjYzOTU4.DylumQ.wPV5QVD_mPYAiRQucfBYaYHSHZ4
# id 537470932420263958
# permission 67648
# https://discordapp.com/oauth2/authorize?client_id=537470932420263958&scope=bot&permissions=67648
import discord
from discord.ext import commands

TOKEN = "NTM3NDcwOTMyNDIwMjYzOTU4.DylumQ.wPV5QVD_mPYAiRQucfBYaYHSHZ4"
client = commands.Bot(command_prefix='!')


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
async def info(ctx):
    await ctx.send(f'```\n'
                   f'!exit: Exit the program\n'
                   f'!count: Count the number of member in guild\n'
                   f'!report: Report the status of member in guild\n'
                   f'!repeat: Repeat what you have just entered\n'
                   f'!clear: Clear the channel\n```')


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


client.run(TOKEN)
