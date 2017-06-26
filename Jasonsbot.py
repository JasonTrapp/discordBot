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




#TODO FIX NONE EXISTANT MEMBER
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
async def getChannels(ctx):
    for server in client.servers:
        for channel in server.channels:
            await client.say(channel)

@client.command(pass_context = True)
async def arith(ctx, symbol, firstVal=None, secondVal=None, *args):
    """
    Perform arithmetic operations: +, -, *, /. Must provide 2 numbers to calculate.
    
    Must be of the form: .arith operation value1, value2, ..., valuen
    valuen being the nth number entered
    """
    if firstVal == None or secondVal == None or type(firstVal) is not float or type(secondVal) is not float:
        await client.say(ctx.message.author.mention + ": Input is of the form 'operation num1 num2 ...'")
        return
    
    if symbol != "+" and symbol != "*" and symbol != "-" and symbol != "/":
        await client.say(ctx.message.author.mention + ": Operations accepted are +, -, * and /")
        return

    flagSymbol = False
    if symbol == "*":
        value = int(firstVal) * int(secondVal)
    elif symbol == "-":
        value = int(firstVal) - int(secondVal)
    elif symbol == "/":
        value = int(firstVal) / int(secondVal)
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
            value -= int(arg)
            
    await client.say(value)


@client.command()
async def leave():
    try:
        await client.disconnect()
    except:
        print("Error disconnecting")

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
    

#####ADMIN FUNCTIONS#####
            
#CLEAN CHAT LAST N MESSAGES
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

#Save contents of announcements
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
async def kickMember(ctx, member: discord.Member = None):
    if member == None:
        await client.say(ctx.message.author.mention + ": Please specify a user to kick.")
        return

    await client.kick(member)
    await client.say(member.mention + " has been kicked from the server.")

client.run('MzI3MDQ1NjI0NDAwOTY5NzI4.DC-nBA.jS3JRACpZMtczaweyZwPoh27kUU')
