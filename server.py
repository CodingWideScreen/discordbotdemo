
from classes.logs import Logs
import discord
from discord.ext.commands import Bot
import os
import requests 
import json
import atexit
import re 
from colorama import deinit, Fore, Back, Style
import asyncio
import ctypes
from datetime import datetime, date


#Evironment 
BOT_TOKEN = '' #token from discord here for your bot

bot = Bot(command_prefix='!',case_insensitive=True)#Sets command prefix; ex. !cat 
logger = Logs('server')

#Bot Events
@bot.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW("DiscordBot")
    # init()#Init our colored terminal
    logger.log("Discord bot up and running..", Fore.LIGHTGREEN_EX)
    await initial_activity(name="Starting up engines") 

@bot.event
async def on_message(message):
    try:
        #Don't want never ending loop as the bot could pick up its own output
        if message.author == bot.user:
            return
        #Process commands, could add whitelist allowing certain users
        await bot.process_commands(message)
    except Exception as e:             
        logger.log(f"Exception occurred :: {repr(e)}", Fore.RED)   

@bot.event
async def on_disconnect():
    logger.log("Client disconnected.")

@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    logger.log(f"Message deleted: {message.content}", Fore.RED)
    
@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user :
        return
    logger.log(f"User {before.author} edited message {before.content} to {after.content}", Fore.YELLOW)           
#End Bot Events

#Functions    
def exit_handler():
    deinit()
    logger.log("Bot terminated.", Fore.RED)      

async def initial_activity(name="Starting up engines", activity=discord.ActivityType.playing):   
    await bot.change_presence(activity=discord.Activity(name=name, type=activity))

# Commands

@bot.command() #await ban(user, *, reason=None, delete_message_days=1)
async def kill(ctx):
    try:
        await bot.logout()
    except Exception as e:             
        logger.log(f"Exception occurred :: {repr(e)}", Fore.RED)         
        

@bot.command()
async def echo(ctx, message: str):
    await ctx.send(message)

atexit.register(exit_handler) 
#Run bot
bot.run(BOT_TOKEN)

