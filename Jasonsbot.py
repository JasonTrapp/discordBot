import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.errors import *
from pprint import pprint

import requests
import asyncio
import logging
import random as rand
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import re


replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'tan' : 'np.tan',
    'exp' : 'np.exp',
    'sqrt' : 'np.sqrt',
    '^': '**',
    'pi' : 'np.pi'
}

allowed_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    'cosh',
    'sinh',
    'tanh',
    'pi'
]

client = discord.Client()
bot_prefix = "."
client = commands.Bot(command_prefix=bot_prefix)

###########################
########## EVENTS #########
###########################
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_member_join(member : discord.Member):
    for server in client.servers:
        for channel in server.channels:
            if channel.name == 'general':
                await client.send_message(channel, "Welcome to the server, " +  member.mention)
                return

@client.event
async def on_member_remove(member : discord.Member):
    for server in client.servers:
        for channel in server.channels:
            if channel.name == 'general':
                await client.send_message(channel,"See ya m8")
                return
    

@client.command(pass_context = True)
async def join(ctx):
    """
    Connects bot to the voice channel user is currently in.
    Keyword arguments:
    ctx -- The non-private channel context
    """
    try:
        await client.join_voice_channel(ctx.message.author.voice_channel)
        await client.say("I am now connected.")
    except InvalidArgument:
        await client.say("Channel doesn't exist.")
    except ClientException:
        await client.say("I'm already connected.")
    except asyncio.TimeoutError:
        await client.say("Could not connect in time.")

@client.command(pass_context = True)
async def leave(ctx):
    """
    Disconnects bot from voice channel.
    Keyword arguments:
    ctx -- The non-private channel context
    """
    try:
        for voice in list(client.voice_clients):
            try:
                await voice.disconnect()
            except:
                pass
    except:
        await client.say("Error disconnecting")
        

###########################
###### MISCELLANEOUS ######
###########################
@client.command(pass_context = True)
async def avatar(ctx, member : discord.Member = None):
    """
    Gets the users avatar url.
    Keyword arguments:
    ctx -- The non-private channel context
    member -- The member in question, if none then the author
    """
    try:
        if(member == None):
            await client.say(ctx.message.author.avatar_url)
        else:
            await client.say(member.avatar_url)
    except:
        await client.say("User does not have an avatar.")

@client.command(pass_context = True)
async def weather(ctx, location : str = None):
    """
    Gets the weather of a city.
    
    """
    if location == None:
        await client.say("You didn't enter a city to get the temperature of.")
        return

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+location+'&APPID=8b49f55c9cc65904c99181f3bf4ebab6')
    
    await client.say('%.2f' % (r.json().get('main').get('temp') - 273.15))

###########################
###### Math COMMANDS ######
###########################
@client.command(pass_context = True)
async def calc(ctx, ops=None):
    """
    A basic calculator to compute the values entered
    Keyword arguments:
    ctx -- The non-private channel context
    ops -- The operations and operands to compute
    """
    try:
        if ops == None:
            await client.say("Please enter something to compute.")
            return

        for word in re.findall('[a-zA-Z_]+', ops):
            if word not in allowed_words:
                raise ValueError(
                    '"{}" is forbidden to use in math expression'.format(word)
                )

        for old, new in replacements.items():
            ops = ops.replace(old, new)

        ops = eval(ops)        
        if abs(ops) < 1e-10:
            await client.say("0")
            return
        
        await client.say(ops)
    except:
        await client.say("An illegal operation has been entered.")
    

@client.command(pass_context = True)
async def plot(ctx, function=None, x1=-10, x2=10):
    """
    Uses matplotlib to plot a mathematical function with respect to x.
    Keyword arguments:
    ctx -- The non-private channel context
    function -- The function to be plotted
    x1 -- The x-value to start at
    x2 -- The x-value to end at
    """
    if function == None:
        await client.say("Please enter a function to be evaluated.")
        return
    
    func = helper(function)
    a = float(x1)
    b = float(x2)

    x = np.linspace(a, b, 250)

    fig1 = plt.gcf()
    plt.plot(x, func(x))
    plt.xlim(a,b)

    fig1.savefig('plot.png',bbox_inches='tight')    
    await client.send_file(ctx.message.channel, "/home/jason/Documents/Programming/python/discordBot/plot.png")
    plt.gcf().clear()

def helper(function):
    for word in re.findall('[a-zA-Z_]+', function):
        if word not in allowed_words:
            raise ValueError(
                '"{}" is forbidden to use in math expression'.format(word)
            )

    for old, new in replacements.items():
        function = function.replace(old, new)
    print(function)
    def func(x):
        return eval(function)

    return func

###########################
####### FUN COMMANDS ######
###########################
@client.command(pass_context = True)
async def kill(ctx, member: discord.Member = None):
    """
    Kill a specified user
    Keyword arguments:
    ctx -- The non-private channel context
    member -- The member to kill
    """
    if member is None:
        await client.say(ctx.message.author.mention + ": I can't kill someone unless you give me a name.")
        return
           
    if member.id == client.user.id:
        await client.say(ctx.message.author.mention + ": Why do you want me to kill myself?")
    elif member.id == ctx.message.author.id:
        await client.say(ctx.message.author.mention + ": Why do you want to die?")
    else:
        await client.say(ctx.message.author.mention + ": Killing " + member.mention)
        
@client.command(pass_context = True)
async def ball(ctx, command: str = None):
    """
    8ball which determines the probability of something happening.
    Keyword arguments:
    ctx -- The non-private channel context
    command -- The string in which the 8ball determines the probability will occur
    """
    if command == None:
        await client.say(ctx.message.author.mention + ", please enter a question.")
        return

    val = rand.randint(1,6)
    if val == 1:
        await client.say("It is impossible that will happen.")
    elif val == 2:
        await client.say("It is unlikely that will happen.")
    elif val == 3:
        await client.say("It is possible that might happen.")
    elif val == 4:
        await client.say("I am certain that will happen.")
    elif val == 5:
        await client.say("Ask me again later.")
    else:
        await client.say("I don't feel like answering.")
    
###########################
##### ADMIN FUNCTIONS #####
###########################
@client.command(pass_context = True)
async def clearChat(ctx, number=None):
    """
    function which clears the last n messages in the current channel
    Keyword arguments:
    ctx -- The non-private channel context
    number -- The number of lines to clear.
    """
    if number == None:
        await client.say("The format of this command is '.clearChat number'. Lines being the number of lines")
        return

    messages = []
    number = int(number)
    if number > 100:
        number = 100
    
    async for i in client.logs_from(ctx.message.channel, limit = number):
        messages.append(i)
        
    await client.delete_messages(messages)

@client.command(pass_context = True)
async def saveMessages(ctx, fileName=None):
    """
    Function which saves all messages in the current channel.
    Keyword arguments:
    ctx -- The non-private channel context.
    fileName -- The filename to store the messages in.
    """
    try:
        if fileName == None:
            await client.say("The format of this command is '.saveMessages myFile'")
            return
        
        file = open(fileName + ".txt", "w")
        await client.delete_message(ctx.message)
        messages = []
        counter = 0
        async for i in client.logs_from(ctx.message.channel, limit=100):
            messages.append(i)
            counter += 1

        for count in range(counter-1, -1, -1):
            file.write(str(messages[count].timestamp.date()) + "\n")
            file.write(messages[count].content + "\n")

        file.close()
        return
    
    except OSError:
        await client.say("File cannot be opened.")    

@client.command(pass_context = True)
async def kickMember(ctx, member: discord.Member = None, reason = "private reasons"):
    """
    Function that kicks a user
    Keyword arguments:
    ctx -- The non-private channel context
    member -- The member to kick
    reason -- The reason for kicking a member
    Exception thrown when user doesn't have permission
    """
    try:
        flag = False
        for perms in ctx.message.author.server_permissions:
            if perms[0] == 'kick_members' and perms[1]:
                flag = true
                break

        if not flag:
            await client.say(ctx.message.author.mention + ": You do not have permission to kick this user.")
            return
        
        if member == None:
            await client.say(ctx.message.author.mention + ": Please specify a user to kick.")
            return
        elif member == ctx.message.author:
            await client.say(ctx.message.author.mention + ": You cannot kick yourself.")
            return
        
        await client.kick(member)
        if reason == ".":
            await client.say(member.mention + " has been kicked from the server.")
        else:
            await client.say(member.mention + " has been kicked from the server for " + reason + ".")
    except Forbidden:
        await client.say(ctx.message.author.mention + ": Bot does not have permission to kick this user.")
    except HTTPException:
        await client.say("Something went wrong, please try again.")
    
@client.command()
async def dc():
    """
    Disconnects the bot from the server.
    Need to restart the program for bot to join
    """
    await client.say("Good night.")
    await client.close()

@client.command(pass_context = True)
async def banMember(ctx, member : discord.Member = None, days = 1, reason = "private reasons"):
    """
    Bans specified member from the server.
    Keyword arguments:
    ctx -- The non-private channel context
    member -- The member to be banned.
    days -- Number of days to ban a user
    reason -- reason for banning a user
    """
    try:
        flag = False
        for perms in ctx.message.author.server_permissions:
            if perms[0] == 'ban_members' and perms[1]:
                flag = true
                break

        if not flag:
            await client.say(ctx.message.author.mention + ": You do not have permission to ban this user.")
            return
        
        if member == None:
            await client.say(ctx.message.author.mention + ", please specify a member to ban.")
            return

        if member.id == ctx.message.author.id:
            await client.say(ctx.message.author.mention + ", you cannot ban yourself.")
        else:
            await client.ban(member, days)
            if reason == ".":
                await client.say(member.mention + " has been banned from the server.")
            else:
                await client.say(member.mention + " has been banned from the server for " + reason + ".")
        return

    except Forbidden:
        await client.say("The bot does not have the necessary permissions to ban someone.")
        return
    except HTTPException:
        await client.say("Something went wrong, please try again.")
        
    

client.run('MzMxNjY0NzM5NjkwMzQ4NTY0.DDy2gw.j3ufZBqM-bgm9i74t8u14qDjMk4')
