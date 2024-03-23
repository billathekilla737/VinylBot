from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore
from Assets.Utilities import Parse_Private
from Assets.VinylScraper import *
import pytz





def run_discord_bot():

    ###########Initialize Bot####################################
    #scrape_race_info()                                         #
    token, URL = Parse_Private()                                #
    #Set the bot's status                                       #
    tree = app_commands.CommandTree(client)                     #
    client = commands.Bot(command_prefix='/', intents=intents)  #
    #bot = commands.Bot(command_prefix='/', intents=intents)    #
    nameList, roleList = Grab_Files()                           #
    RacesJson = 'Daddy-Bot-env/Assets/F1Information.json'       #
    url = 'https://www.reddit.com/r/VinylReleases/new/'         #
    #############################################################




    async def on_ready():
            #Variable Initialization
            #####################################################################
            print('We have logged in as {0.user}'.format(client))
            await client.change_presence(activity=discord.Game("with your moms's record player"))

            
            while True:
                  pass
                  await asyncio.sleep(45)















    client.run(token) 
run_discord_bot()  