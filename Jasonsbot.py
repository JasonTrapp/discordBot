import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import logging

client = discord.Client()
bot_prefix = "."
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.command()
async def hello(*args):
    await client.say("Hello")

#TODO
@client.command(pass_context = True)
async def kill(ctx, *, member: discord.Member = None):
    if member is None:
        await client.say(ctx.message.author.mention + ": I can't kill someone unless you give me a name.")
        return
    try:
        if member.id == client.user.id:
            await client.say(ctx.message.author.mention + ": Why do you want me to kill myself?")
        elif member.id == ctx.message.author.id:
            await client.say(ctx.message.author.mention + ": Why do you want to die?")
        else:
            await client.say(ctx.message.author.mention + ": Killing " + member.mention)
    except Exception:
        await client.say(ctx.message.author.mention + ", the mentioned user does not exist.")
    else:
        await client.say(ctx.message.author.mention + ", the mentioned user does not exist.")

#TODO
@client.command(pass_context = True)
async def getAllMembers(ctx, *args):
    for obj in discord.Server(*args).members:
        await client.say(obj.id)

@client.command(pass_context = True)
async def getChannels(ctx):
    for server in client.servers:
        for channel in server.channels:
            await client.say(channel)

@client.command(pass_context = True)
async def arith(ctx, symbol, *args):
    flagSymbol = False
    if symbol == "*" or symbol == "/":
        value = 1
    else:
        value = 0

    for arg in args:
        if symbol == "+":
            value += int(arg)
        elif symbol == "*":
            value *= int(arg)
        elif symbol == "/":
            value /= float(arg)
        elif symbol == "-":
            pass
        else:
            flagSymbol = True
            break

    if symbol == "+" or symbol == "*" or symbol == "-" or symbol == "/":
        await client.say(value)
    else:
        await client.say(ctx.message.author.mention + ": You did not enter a valid operation.")

#####ADMIN FUNCTIONS#####
            
#CLEAN CHAT LAST N MESSAGES
@client.command(pass_context = True)
async def clearChat(ctx, number):
    messages = []
    number = int(number)
    async for i in client.logs_from(ctx.message.channel, limit = number):
        messages.append(i)
        
    deleted = await client.delete_messages(messages)

#Save contents of announcements
@client.command(pass_context = True)
async def saveAnnouncements(ctx, saveMessage: str):
    file = open("announcement.txt", "w")
    await client.delete_message(ctx.message)
    messages = []
    counter = 0
    async for i in client.logs_from(ctx.message.channel, limit=100):
        messages.append(i)
        counter += 1

    for count in range(counter-1, -1, -1):
        file.write(messages[count].content + "\n")

    file.close()

#Save contents of rules
@client.command(pass_context = True)
async def saveRules(ctx, saveRules: str):
    file = open("rules.txt", "w")
    await client.delete_message(ctx.message)
    messages = []
    counter = 0
    async for i in client.logs_from(ctx.message.channel, limit=100):
        messages.append(i)
        counter += 1

    for count in range(counter-1, -1, -1):
        file.write(messages[count].content + "\n")
        
    file.close()

client.run('token')
