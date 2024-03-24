from discord.ext import commands, tasks
from Assets.Utilities import *
from Assets.VinylScraper import *
from Assets.UserCommands import *
import discord 
import asyncio
import json






def run_discord_bot():
    token, URL = Parse_Private()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='/', intents=intents)

    # Load the UserCommands module as an extension
    
    

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        await bot.change_presence(activity=discord.Game("with your mom's record player"))
        
    bot.load_extension('Assets.UserCommands')
    bot.run(token)

if __name__ == "__main__":
    run_discord_bot()


#Commented Out for Testing Purposes
##########################################################################################################
model  = "gpt-3.5-turbo-0125"
#GPT_Prompt = "Given a list of subreddit post titles about vinyl album releases, your task is to analyze these titles, which are user-generated and may contain duplicates or different wordings for the same release. Your objective is to identify unique releases, disregard exact duplicates and near-duplicates, and output a processed list with unique album releases. Consider variations in color as unique and include them in the processed list. Use your understanding of natural language to interpret varied expressions and terminologies users might use to describe the same album. Occasionally you will be given an empty list. In this case, please output 'No new releases found.'"
Duplicate_Removal_Prompt = """
Given a list of subreddit post titles about vinyl album releases, your task is to analyze these titles, 
which are user-generated and may contain duplicates or different wordings for the same release. Your objective
is to identify unique releases, taking special care to retain the full title of each release, including the 
artist's name, album title, and any unique descriptors such as edition, color variant, or special edition details.
Disregard exact duplicates and near-duplicates, but variations in color or edition are considered unique and should
be included in the processed list. Use your understanding of natural language to interpret varied expressions
and terminologies users might use to describe the same album. If you are given an empty list, output 
'No new releases found.' It's crucial to keep the artist's name as part of the album's description in 
your output to ensure clarity and completeness. Organize the final result alphabetically.
"""


SearchArtistPrompt = """
You are given two lists. The first list contains artists or albums. 
The second list contains a variety of artists or albums from a different source. Your task is to compare these 
two lists and identify any entries that appears in both.The matches may not always be exact as they are user generated
When you find matches, output them clearly. If there are no matches, respond with "No matches found." Ensure accuracy by 
paying close attention to the details of each entry, as there may be slight variations in how artist names or album titles are presented. 
Use your understanding of artist names and album titles to make accurate comparisons even when faced with minor differences in spelling or formatting.
"""

#Dupes_Removed = RemoveDuplicates(get_recent_posts(80), Duplicate_Removal_Prompt, model)
#print(Dupes_Removed)
#

# Load the JSON data from 'SearchParms.json'
# with open('Assets/SearchParams.json', 'r') as file:
#     data = json.load(file)

# all_artists = []
# for user_likes in data.values():
#     all_artists.extend(user_likes)

# # The 'all_artists' list now contains all the artist names
# print(json.dumps(all_artists, indent=2))


