import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.errors import *

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

@client.command()
async def hello(*args):
    await client.send_message(message.channel, "Hello")

@client.command(pass_context = True)
async def join(ctx):
    """
    Connects bot to the voice channel user is currently in.
    """
    try:
        await client.join_voice_channel(ctx.message.author.voice_channel)
        await client.say("I am now connected.")
    except InvalidArgument:
        await client.say("Channel doesn't exist.")
        return
    except ClientException:
        await client.say("I'm already connected.")
        return
    except asyncio.TimeoutError:
        await client.say("Could not connect in time.")
        return

@client.command(pass_context = True)
async def leave(ctx):
    """
    Disconnects bot from voice channel.
    """
    try:
        for voice in list(client.voice_clients):
            try:
                await voice.disconnect()
            except:
                pass
    except:
        await client.say("Error disconnecting")
        return

###########################
###### MISCELLANEOUS ######
###########################
@client.command(pass_context = True)
async def avatar(ctx, member : discord.Member = None):
    try:
        if(member == None):
            await client.say(ctx.message.author.avatar_url)
            return
        else:
            await client.say(member.avatar_url)
    except:
        await client.say("User does not have an avatar.")
        return

@client.command()
async def Help():
    await client.say(".join - bot joins the users voice channel.")
    await client.say(".leave - bot disconnects from voice channel.")
    await client.say(".plot function x1 x2 - x1 and x2 are optional")
    await client.say(".kill user - Tell the bot to kill a user.")
    await client.say(".ball question - Determine the probability of an event happening.")
    await client.say(".clearChat n - clear n lines from chat.")
    await client.say(".saveMessages filename - saves all messages in channel to a text file")
    await client.say(".kickMember user - kick user from the server")

###########################
###### Math COMMANDS ######
###########################
@client.command(pass_context = True)
async def calc(ctx, ops=None):
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
        return
    except:
        await client.say("An illegal operation has been entered.")
    

@client.command(pass_context = True)
async def plot(ctx, function=None, x1=-10, x2=10):
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
    """
    if command == None:
        await client.say(ctx.message.author.mention + ", please enter a question.")
        return

    val = rand.randint(1,6)
    if val == 1:
        await client.say("It is impossible that will happen.")
        return
    elif val == 2:
        await client.say("It is unlikely that will happen.")
        return
    elif val == 3:
        await client.say("It is possible that might happen.")
        return
    elif val == 4:
        await client.say("I am certain that will happen.")
        return
    elif val == 5:
        await client.say("Ask me again later.")
        return
    else:
        await client.say("I don't feel like answering.")
        return
    
###########################
##### ADMIN FUNCTIONS #####
###########################
@client.command(pass_context = True)
async def clearChat(ctx, number=None):
    """
    function which clears the last n messages in the current channel
    Parameters:
        number: The number of lines to be removed
    """
    if number == None:
        await client.say("The format of this command is '.clearChat number'. Lines being the number of lines")
        return
    
    messages = []
    number = int(number)
    async for i in client.logs_from(ctx.message.channel, limit = number):
        messages.append(i)
        
    deleted = await client.delete_messages(messages)

@client.command(pass_context = True)
async def saveMessages(ctx, fileName=None):
    """
    Function which saves all messages in the current channel.
    Argument received is the name of the file to be stored.
    """
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

@client.command(pass_context = True)
async def kickMember(ctx, member: discord.Member = None, reason = "."):
    """
    Function that kicks a user
    Exception thrown when user doesn't have permission
    """
    try:
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
        await client.say(ctx.message.author.mention + ": You do not have permission to kick this user.")
        return
    except HTTPException:
        await client.say("Something went wrong, please try again.")
        return
    
@client.command()
async def dc():
    """
    Disconnects the bot from the server.
    Need to restart the program for bot to join
    """
    await client.say("Good night.")
    await client.close()

@client.command(pass_context = True)
async def banMember(ctx, member : discord.Member = None, days = 1, reason = "."):
    """
    Bans specified member from the server.
    """
    try:
        if member == None:
            await client.say(ctx.message.author.mention + ", please specify a member to ban.")
            return

        if member.id == ctx.message.author.id:
            await client.say(ctx.message.author.mention + ", you cannot ban yourself.")
            return
        else:
            await client.ban(member, days)
            if reason == ".":
                await client.say(member.mention + " has been banned from the server.")
            else:
                await client.say(member.mention + " has been banned from the server for " + reason + ".")
            return
    except Forbidden:
        await client.say("You do not have the necessary permissions to ban someone.")
        return
    except HTTPException:
        await client.say("Something went wrong, please try again.")
        
    

client.run('MzI3MDQ1NjI0NDAwOTY5NzI4.DC-nBA.jS3JRACpZMtczaweyZwPoh27kUU')
