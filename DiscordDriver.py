from discord import app_commands
from discord.ext import commands
from Assets.Utilities import *
from Assets.VinylScraper import *
import discord 
import asyncio






def run_discord_bot():

    ###########Initialize Bot####################################
    token, URL = Parse_Private()                                #
    #Set the bot's status                                       #
    intents = discord.Intents.all()                             #
    client = commands.Bot(command_prefix='/', intents=intents)  #
    #############################################################



    @client.event
    async def on_ready():
            #Variable Initialization
            #####################################################################
            print('We have logged in as {0.user}'.format(client))
            await client.change_presence(activity=discord.Game("with your moms's record player"))

            
            while True:
                recent_posts = get_recent_posts(50)
                print(recent_posts)





                await asyncio.sleep(1800)






    client.run(token) 
run_discord_bot()  