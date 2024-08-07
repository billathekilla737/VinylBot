from discord.ext import commands
from discord import app_commands
from Assets.Utilities import *
from Assets.VinylScraper import *
import discord 
import json
import tabulate
import asyncio

#Commented Out for Testing Purposes
##########################################################################################################

#model  = "gpt-3.5-turbo-0125"
model = "gpt-4o" #Newer More Expensive Model, Higher Accuracy

# Duplicate_Removal_Prompt = """
# Given a list of post titles about vinyl album releases, your task is to analyze these titles, 
# which are user-generated and may contain duplicates or different wordings for the same release. Your objective
# is to identify unique releases, taking special care to retain the full title of each release, including the 
# artist's name, album title, and any unique descriptors such as edition, color variant, or special edition details.
# It is very important NOT to include near duplicates, any near duplicates should be compressed into one entry not multiple
# lean on the side of strictness when deciding of two color variants are the same if a color repeats at all don't include it.
# If you are given an empty list, output 'No new releases found.' It's crucial to keep the artist's name as part of the album's description in 
# your output to ensure clarity and completeness. Organize the final result alphabetically and only include the data as csv's nothing else.
# """
Duplicate_Removal_Prompt = """
1. **Identify Unique Releases**: Disregard exact duplicates and near-duplicates. Variations in color, edition, or special descriptors should be considered unique and included in the final list. However, each unique color or edition should only appear once, regardless of slight differences in wording.
2. **Full Titles**: Retain the full title of each release, including artist's name, album title, and unique descriptors.
3. **Strict Duplicate Handling**: Be strict in identifying and compressing near duplicates. If a color variant or edition repeats in any form, do not include it more than once.
4. **Uncolored Version Inclusion**: Ensure that the uncolored version (non-special edition or color variant) of each album is included if it exists.
5. **Duplicate Color Handling**: If a variation attribute repeats in any way in the titles, do not include it more than once in the final list. The ONLY exception is to include the uncolored version of the album if it exists. The uncolored version will not have any color attributes in the title.
6. **Include Unique Variations**: Ensure that for each album, one unique colored variation and one uncolored version (if it exists) are included in the final list.
7. **Check For Repeats** against from the history list provided to make sure they are not being repeated.
8. **Output Format**: Organize the final result alphabetically by artist's name and album title. Only include the data as CSV format, with each entry on a new line.
"""
SearchArtistPrompt = """
You are given two lists. The first list contains artists or albums. 
The second list contains a variety of artists or albums from a different source. Your task is to compare these 
two lists and identify any entries that appears in both.They may not match perfectly due to the variations in spelling and formatting, use your 
understanding of natural language to identify matches. When you find matches, output them clearly as comma seperated values make sure to include both the artist name and any other information in the post title.
If there are no matches, respond with ONLY "No matches found." 
"""

#TODO: Add some sort of burst detecting for when everyone post the same thing for a few days.
#continued...We will Keep the last post sets for three days and compare it's names the the last three days to remove repeats.



def run_discord_bot():

    token, URL = Parse_Private()
    intents = discord.Intents.all()
    client = discord.Client(command_prefix='/', intents=intents)
    tree = app_commands.CommandTree(client)
    


    @client.event
    async def DelayedLoop(Vinylchannel):
        PostList = "Init#1"
        postSearchAmount = 30 #Post
        MinutesTillSearch = 2 #Minutes
        PostHistory = extract_titles(Read_Variation_Data())
        while True:
            try:
                #TODO: Mod Try Except to the get_recent_posts function to clean up the code
                PostList = await get_recent_posts(postSearchAmount)  # Await the async function
            except Exception as e:
                print(e)
                PostList = []

            with open('Assets/SearchParams.json', 'r') as file:
                data = json.load(file)
            # Dump all the artist into a python list
            all_artists = [artist for user_likes in data.values() for artist in user_likes]
             
            if PostList:
                try:
                    #TODO: We are going to cross refence  the new post found with the last week of posts to remove duplicates. The 
                    #Grab just the titles from the post list
                    posts_without_duplicates = RemoveDuplicates(preprocess_input(PostList), Duplicate_Removal_Prompt, model, PostHistory)
                    cleaned_posts_list = convert_to_list(posts_without_duplicates)
                    matches = SearchArtist(all_artists,cleaned_posts_list, model, SearchArtistPrompt)
                    Store_Varation_Data(matches)
                except Exception as e:
                    print(e)
                    matches = "API Error. Please try again later."
                    
                if matches.strip() and matches not in ["No matches found.", "API Error. Please try again later."]:
                    # Attempt to see if we can find everyone who likes the match in the JSON file and tag them
                    matched_users = {}
                    normalized_matches = normalize_string(matches)
                    for user, liked_artists in data.items():
                        matched_artists = [artist for artist in liked_artists if normalize_string(artist) in normalized_matches]
                        if matched_artists:
                            matched_users[user] = matched_artists
                    
                    if matched_users:
                        table_rows = [["User", "Matched Artists", "Variation"]]
                        for user, user_matches in matched_users.items():
                            variations = []
                            for artist in user_matches:
                                for line in matches.split(','):
                                    if normalize_string(artist) in normalize_string(line):
                                        variations.append(line.strip())
                            table_rows.append([f"@{user}", ", ".join(user_matches), "\n".join(variations)])
                            table_rows.append(["", "", ""])  # Add an empty row for spacing
                        
                        table = tabulate.tabulate(table_rows, headers="firstrow", tablefmt="pipe")
                        matches = f"Hey {' '.join([f'@{user}' for user in matched_users.keys()])}, I found a match for you:\n\n```{table}```"
                    else:
                        matches = f"I found a match for you: {matches}"
                    
                    # Send the message to the Vinylchannel
                    await Vinylchannel.send(matches)
                    ############################################################################################################
                
            else:
                print(f"No matches found. at {datetime.now().strftime('%I:%M:%S %p')} waiting {MinutesTillSearch} minutes")
            await asyncio.sleep(MinutesTillSearch * 60) #<-For some reason this can't me moved to utilities.py
    
    async def HistoryCleaner(Keep_For):
        #Every 12Hr we will clean the history list of anything older than our Keep_For variable
        while True:
            CleanedItems = Remove_Variation_History(Keep_For)
            print(f"Cleaned Items: {CleanedItems}")
            await asyncio.sleep(60*60*12) #12Hr
    
    @client.event
    async def on_ready():
        Keep_For = 7 #Days
        Vinylchannel = client.get_channel(1217119273684701354)
        Testchannel = client.get_channel(1115817757267730533)
        Channel = Vinylchannel
        print(f'We have logged in as {client.user}')
        await client.change_presence(activity=discord.Game("with your mom's record player"))

        try:
            synced = await tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)
        client.loop.create_task(DelayedLoop(Channel))
        #TODO: Make another loop that runs once every 12hr to clear the anything older than 7 days from the history list.
        client.loop.create_task(HistoryCleaner(Keep_For))
        

    #Slash Commands
    ############################################################################################################
    @tree.command(name="addartist", description="Add an artist to your liked artists list")
    async def Add_User_Liked_Artist(interaction: discord.Interaction, artist:str):
        #Grab the name of the person who called the command
        user = interaction.user
        #Load the JSON data from 'SearchParams.json'
        with open('Assets/SearchParams.json', 'r') as file:
            data = json.load(file)
        #Check if the user is already in the JSON file
        if user.name in data:
            if artist in data[user.name]:
                await interaction.response.send_message(f"{user.name} already likes {artist}", ephemeral=True)
            else:
                data[user.name].append(artist)
                with open('Assets/SearchParams.json', 'w') as file:
                    json.dump(data, file)
                await interaction.response.send_message(f"{user.name} has added {artist} to the list of liked artists", ephemeral=True)
        else:
            data[user.name] = [artist]
            with open('Assets/SearchParams.json', 'w') as file:
                json.dump(data, file)
            await interaction.response.send_message(f"{user.name} has added {artist} to the list of liked artists", ephemeral=True)


    @tree.command(name="removeartist", description="Remove an artist from your liked artists list")
    async def Remove_User_Liked_Artist(interaction: discord.Interaction, artist:str):
        #Grab the name of the person who called the command
        user = interaction.user
        #Load the JSON data from 'SearchParams.json'
        with open('Assets/SearchParams.json', 'r') as file:
            data = json.load(file)
        #Check if the user is already in the JSON file
        if user.name in data:
            if artist in data[user.name]:
                data[user.name].remove(artist)
                with open('Assets/SearchParams.json', 'w') as file:
                    json.dump(data, file)
                await interaction.response.send_message(f"{artist} has been removed from the list of liked artists", ephemeral=True)
            else:
                await interaction.response.send_message(f"{user.name} does not like {artist}", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.name} has not liked any artists yet", ephemeral=True)

    @tree.command(name="listartists", description="List all the artists you like")
    async def List_User_Liked_Artists(interaction: discord.Interaction):
        #Grab the name of the person who called the command
        user = interaction.user
        #Load the JSON data from 'SearchParams.json'
        with open('Assets/SearchParams.json', 'r') as file:
            data = json.load(file)
        #Check if the user is already in the JSON file
        if user.name in data:
            await interaction.response.send_message(f"{user.name} likes the following artists: {', '.join(data[user.name])}", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.name} has not liked any artists yet", ephemeral=True)
    
       

    @tree.command(name="help", description="Tells you the commands for the bot")
    async def help(interaction: discord.Interaction):
        # Define the table headers
        headers = ["Command", "Description"]
        rows = [
            ["/addartist", "Add an artist to your liked artists list"],
            ["/removeartist", "Remove an artist from your liked artists list"],
            ["/listartists", "List all the artists you like"],
            ["/help", "Tells you the commands for the bot"]

        ]
        table = tabulate(rows, headers=headers, tablefmt="pipe")
        await interaction.response.send_message(f"Here are the available commands:\n\n```{table}```")

    client.run(token)

if __name__ == "__main__":
    run_discord_bot()