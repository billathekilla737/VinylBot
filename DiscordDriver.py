from discord.ext import commands
from discord import app_commands
from Assets.Utilities import *
from Assets.VinylScraper import *
import discord 
import asyncio
import json
import tabulate
import warnings
from datetime import datetime

#Commented Out for Testing Purposes
##########################################################################################################
warnings.filterwarnings("ignore", category=UserWarning)
model  = "gpt-3.5-turbo-0125"
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

#TODO: Make the ViewedPost.txt a JSON file so that it will pursist through github pushes
#TODO: Make it so that when I pass the artist list to CHATGPT, the User who likes it is passed too. That way I can say "Hey @User, I found a match for you"

def run_discord_bot():

    token, URL = Parse_Private()
    intents = discord.Intents.all()
    client = discord.Client(command_prefix='/', intents=intents)
    tree = app_commands.CommandTree(client)
    


    
    @client.event
    async def on_ready():
        current = "Init#1"
        last = "Init#2"
        postSearchAmount = 50
        MinutesTillSearch = 45
        Vinylchannel = client.get_channel(1217119273684701354)
        print(f'We have logged in as {client.user}')
        await client.change_presence(activity=discord.Game("with your mom's record player"))

        try:
            synced = await tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)
        

        while True:
            # Every X minutes we will check for 50 new posts
            #TODO Remove Only call the GPT API if there are new posts to check I.E. get_recent_posts() != last
            #Dupes_Removed = RemoveDuplicates(get_recent_posts(postSearchAmount), Duplicate_Removal_Prompt, model)
            #Dupe_Removed_List = convert_to_list(Dupes_Removed)
            current = get_recent_posts(postSearchAmount)

            #We recheck the file for the updated list of artists
            with open('Assets/SearchParams.json', 'r') as file:
                data = json.load(file)
            
            # Dump all the artist into a python list
            all_artists = [artist for user_likes in data.values() for artist in user_likes]

            
            # Perform the search
            if current != last:
                try:
                    Dupes_Removed = RemoveDuplicates(current, Duplicate_Removal_Prompt, model)
                    Dupe_Removed_List = convert_to_list(Dupes_Removed)
                    matches = SearchArtist(all_artists, Dupe_Removed_List, model, SearchArtistPrompt)
                except Exception as e:
                    print(e)
                    matches = "API Error. Please try again later."
            else:
                continue

            #If matches is == to "No matches found." then we will not send a message
            if matches != "No matches found.":
                print(matches)
                last = current
                #Send the message to the Vinylchannel
                await Vinylchannel.send(matches)
            else:
                print("No matches found.")

            # Sleep for X minutes
            #await asyncio.sleep(MinutesTillSearch * 60)
            await asyncio.sleep(30)



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















