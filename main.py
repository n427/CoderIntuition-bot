import os
import discord
from discord.ext import commands, tasks
import asyncio
import time
from datetime import datetime

client = commands.Bot(command_prefix='!')


@client.event 
async def on_ready():
    print("logged in as {0.user}".format (client))
    
@client.command()
async def job(ctx):
    embed=discord.Embed(
   
    title= ":tada: NEW JOB POSTING :tada:",
    color=0x4d69e9)
    embed.add_field(name="Company", value="[company](https://CoderIntuition.com)", inline=False)

    embed.add_field(name="Season", value="season", inline=False)

    embed.add_field(name="Location(s)", value="location", inline=False)

    embed.add_field(name="Notes", value="notes", inline=False)

    now = datetime.now()
    current_time = now.strftime("%I:%M%p \n%D")

    embed.add_field(name="Ingested At", value= current_time, inline=False)
    
    embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")
    
   

    await ctx.send(embed=embed)

my_secret = os.environ['TOKEN']
client.run(my_secret)