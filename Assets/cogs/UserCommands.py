import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to Discord!')
        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def echo(self, ctx, *, content:str):
        await ctx.send(content)

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
    
async def setup(bot):
    await bot.add_cog(UserCommands(bot))