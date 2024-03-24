import discord
import json
from discord.ext import commands

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.SearchFile = 'Assets/SearchParams.json'

    @commands.command()
    async def add_to_list(self, ctx, *, item: str):
        # Get the user ID and add the item to the search list
        user_id = ctx.author.id
        data_entry = {"user_id": user_id, "item": item}

        # Append the new entry to the JSON file
        with open(self.SearchFile, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(data_entry)
            f.seek(0)
            json.dump(data, f, indent=4)

        await ctx.send(f"{item} added to the list along with your Discord user ID, {user_id}.")

    @commands.command()
    async def show_whole_list(self, ctx):
        try:
            with open(self.SearchFile, 'r') as file:
                data = json.load(file)
            await ctx.send(f"Here are all searches:\n```json\n{json.dumps(data, indent=4)}\n```")
        except FileNotFoundError:
            await ctx.send("The search list file was not found.")
        except json.JSONDecodeError:
            await ctx.send("The search list file is empty or corrupted.")


    @commands.command()
    async def help(self, ctx):
        help_message = """
        **Commands:**
        - `/add_to_list [item]`: Add an item to the search list.
        - `/show_whole_list`: Show the entire search list.
        - `/help`: Display this help message.
        """
        await ctx.send(help_message)

def setup(bot):
    bot.add_cog(CommandCog(bot))
