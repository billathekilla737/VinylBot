from discord.ext import commands
from discord import app_commands
from Assets.Utilities import *
from Assets.VinylScraper import *
import discord 
import json
import tabulate
from datetime import datetime

#Commented Out for Testing Purposes
##########################################################################################################

#model  = "gpt-3.5-turbo-0125"
model = "gpt-4o" #Newer More Expensive Model, Higher Accuracy
Duplicate_Removal_Prompt = """
Given a list of subreddit post titles about vinyl album releases, your task is to analyze these titles, 
which are user-generated and may contain duplicates or different wordings for the same release. Your objective
is to identify unique releases, taking special care to retain the full title of each release, including the 
artist's name, album title, and any unique descriptors such as edition, color variant, or special edition details.
Disregard exact duplicates and near-duplicates, but variations in color or edition are considered unique and should
be included in the processed list. Use your understanding of natural language to interpret varied expressions
and terminologies users might use to describe the same album. If you are given an empty list, output 
'No new releases found.' It's crucial to keep the artist's name as part of the album's description in 
your output to ensure clarity and completeness. Organize the final result alphabetically and only include the data as csv's nothing else.
"""
SearchArtistPrompt = """
You are given two lists. The first list contains artists or albums. 
The second list contains a variety of artists or albums from a different source. Your task is to compare these 
two lists and identify any entries that appears in both.They may not match perfectly due to the variations in spelling and formatting, use your 
understanding of natural language to identify matches. When you find matches, output them clearly as comma seperated values with the full match name string. If there are no matches, respond with ONLY "No matches found." 
"""

#TODO: Make the ViewedPost.txt a JSON file so that it will pursist through github pushes
#TODO: Make it so that when I pass the artist list to CHATGPT, the User who likes it is passed too. That way I can say "Hey @User, I found a match for you"

def run_discord_bot():

    token, URL = Parse_Private()
    intents = discord.Intents.all()
    client = discord.Client(command_prefix='/', intents=intents)
    tree = app_commands.CommandTree(client)
    


    @client.event
    async def DelayedLoop(Vinylchannel):
        PostList = "Init#1"
        postSearchAmount = 50 #Post
        MinutesTillSearch = 10 #Minutes
        while True:
            try:
                PostList = await get_recent_posts(postSearchAmount)  # Await the async function
            except Exception as e:
                print(e)
                PostList = []

            with open('Assets/SearchParams.json', 'r') as file:
                data = json.load(file)
            
            # Dump all the artist into a python list
            all_artists = [artist for user_likes in data.values() for artist in user_likes]
            
            # Perform the search if there are any new post detected 
            if PostList:
                try:
                    posts_without_duplicates = RemoveDuplicates(PostList, Duplicate_Removal_Prompt, model)
                    cleaned_posts_list = convert_to_list(posts_without_duplicates)
                    matches = SearchArtist(all_artists,cleaned_posts_list, model, SearchArtistPrompt)
                except Exception as e:
                    print(e)
                    matches = "API Error. Please try again later."
                #If there is a match, send the message to the Vinylchannel
                if matches != "No matches found." and matches != "API Error. Please try again later.":
                    print(f"{matches} at {datetime.now().strftime('%I:%M:%S %p')} waiting {MinutesTillSearch} minutes")
                    
                    # Attempt to see if we can find everyone who likes the match in the JSON file and tag them
                    matched_users = {}
                    for user, liked_artists in data.items():
                        matched_artists = [artist for artist in liked_artists if artist in matches]
                        if matched_artists:
                            matched_users[user] = matched_artists
                    
                    if matched_users:
                        table_rows = [["User", "Matched Artists"]]
                        for user, user_matches in matched_users.items():
                            table_rows.append([f"@{user}", ", ".join(user_matches)])
                        
                        table = tabulate.tabulate(table_rows, headers="firstrow", tablefmt="pipe")
                        matches = f"Hey {' '.join([f'@{user}' for user in matched_users.keys()])}, I found a match for you:\n\n```{table}```"
                    else:
                        matches = f"I found a match for you: {matches}"
                    
                    # Send the message to the Vinylchannel  # Replace with your channel ID
                    await Vinylchannel.send(matches)
                elif matches == "API Error. Please try again later.":
                    print(f"{matches} at {datetime.now().strftime('%I:%M:%S %p')} waiting {MinutesTillSearch} minutes")
                    #Send the message to the Vinylchannel
                    await Vinylchannel.send(matches)
            else:
                print(f"No matches found. at {datetime.now().strftime('%I:%M:%S %p')} waiting {MinutesTillSearch} minutes")
            await asyncio.sleep(MinutesTillSearch * 60) #<-For some reason this can't me moved to utilities.py
    
    @client.event
    async def on_ready():
        
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