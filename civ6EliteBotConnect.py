import os
import discord
from dotenv import load_dotenv
import civ6EliteBot
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

leaders = civ6EliteBot.load_leaders()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='pick')
async def on_message(ctx):
    for leader in civ6EliteBot.random_leaders(leaders, 3):
        response = leader.name + "\n"
        await ctx.send(response, file = discord.File(leader.image_path()))

bot.run(TOKEN)
