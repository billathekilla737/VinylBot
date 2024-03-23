import discord 
import json
from discord.ext import commands

# Initialize the bot
bot = commands.Bot(command_prefix='!')

SearchFile = 'Assets/SearchParams.json'
Search = set()
SearchList = []

# ADD TO LIST FUNCTION
@bot.command()
async def add_to_list(ctx, *, item: str):
    # Get the username of the user who sent the command
    username = ctx.author.name
    # Add the item and username to the Searchlist
    SearchList.append((username, item))
    # Add the item and username to the SearchFile
    with open(SearchFile, 'a') as f:
        f.write(username + ' ' + item + '\n')
    # Send a confirmation message
    await ctx.send(f"{item} added to the list along with your Discord username, {username}.")

@bot.command()
async def show_whole_list(ctx, file_name: str):
    try:
        # Read the contents of the JSON file
        with open(SearchFile, 'r') as file:
            data = json.load(file)
        # Send the contents of the JSON file as a message
        await ctx.send(f"Here are all searches:\n```json\n{json.dumps(data, indent=4)}\n```")
    except FileNotFoundError:
        # If the file is not found, send an error message
        await ctx.send(f"File '{file_name}' not found.")

@bot.command()
async def show_my_list(ctx, file_name: str):
    try:
        # Read the contents of the JSON file
        with open(SearchFile, 'r') as file:
            data = json.load(file)
        # Send the contents of the JSON file as a message
        await ctx.send(f"Here are your searches:\n```json\n{json.dumps(data, indent=4)}\n```")
    except FileNotFoundError:
        # If the file is not found, send an error message
        await ctx.send(f"File '{file_name}' not found.")