import os
import discord
from dotenv import load_dotenv
import civ6EliteBot
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

leaders = civ6EliteBot.load_leaders()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='pick')
async def on_message(ctx, n:int=3):

    if n > 10:
        await ctx.send("T'en demandes trop là!")
        return

    for leader in civ6EliteBot.random_leaders(leaders, n):
        response = leader.name + "\n"
        await ctx.send(response, file = discord.File(leader.image_path()))


selected_msg_id = -1
@bot.command(name='game')
async def on_message(ctx, n:int, p1: discord.Member = None, p2: discord.Member = None, 
 p3: discord.Member = None, p4: discord.Member = None, 
 p5: discord.Member = None, p6: discord.Member = None, 
 p7: discord.Member = None, p8: discord.Member = None):

    players = list(filter(lambda p: p != None, [p1, p2, p3, p4, p5, p6, p7, p8]))
    if len(players) * n > 53:
        await ctx.send("Not enough civilizations!")
        return

    for player in players:
        if players.count(player) > 1:
            await ctx.send("Same player can't play twice!")
            return

    leadersPool = civ6EliteBot.random_leaders(leaders, n * len(players))
    leadersDict = {p: leadersPool[n*i:n*(i+1)] for i, p in enumerate(players)}

    for player in players:
        await ctx.send(f"**{player.name}**'s leaders pool: ")

        leader_msgs = []
        for leader in leadersDict[player]:
            response = leader.name + "\n"
            message_sent = await ctx.send(response, file = discord.File(leader.image_path()))
            leader_msgs.append(message_sent)

        # check lambda function
        def check(reaction, user):
            condition = reaction.message.id in [msg.id for msg in leader_msgs] and user == player
            if condition:
                global selected_msg_id
                selected_msg_id = reaction.message.id
            return condition

        # Wait for reaction, then highlight selected leader
        await bot.wait_for("reaction_add", check=check, timeout=3600.0)
        global selected_msg_id
        if selected_msg_id != -1:
            for leader_msg in leader_msgs:
                fetch_msg = await ctx.channel.fetch_message(leader_msg.id)
                if fetch_msg.id == selected_msg_id:
                    await fetch_msg.edit(content=f"**{fetch_msg.content}**")
                else:
                    await fetch_msg.edit(content=f"~~{fetch_msg.content}~~")      
            selected_msg_id = -1

    await ctx.send("**GLHF!**")

bot.run(TOKEN)
