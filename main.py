import os
import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime
from urllib.request import urlopen
from replit import db
from keep_alive import keep_alive

PST = pytz.timezone("Canada/Pacific")
HEADER_SEPARATOR = "|---|---|---|--|"
PRESENT_STATUS = "Present"
TERM = "Fall 2021"
DATA_URL = "https://raw.githubusercontent.com/BaruYogesh/Fall2021Internships/master/US.md"
CHANNEL_ID = 800553079643570226

client = commands.Bot(command_prefix="!")

# delete the database
# for key in db.keys():
#     try:
#         del db[key]
#     except KeyError:
#         pass
# keys_to_delete = ["Google", "PagerDuty", "Samsung", "Epic Games", "Rubrik", "Zipline"]

# for key in keys_to_delete:
#   del db[key]

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    fetch_postings.start()


async def send_posting(posting):
    if not posting["company"] or not posting[
            "link"] or posting["status"] != "Present":
        return False

    if posting["company"] in db.keys():
        return False

    now = datetime.now(PST)
    current_time = now.strftime("%a %b %d, %Y %-I:%M %p PST")

    db[posting["company"]] = current_time

    embed = discord.Embed(title="New Internship Posting  :tada:",
                          color=0x4d69e9)
    embed.add_field(name="Company", value=posting["company"], inline=False)
    if posting["location"]:
        embed.add_field(name="Location",
                        value=posting["location"],
                        inline=False)
    if posting["term"]:
        embed.add_field(name="Term", value=posting["term"], inline=False)
    if posting["notes"]:
        embed.add_field(name="Notes", value=posting["notes"], inline=False)
    embed.add_field(name="Posting Time", value=current_time, inline=False)
    embed.add_field(name="Application Link",
                    value=posting["link"],
                    inline=False)
    embed.set_footer(text="Internship Job Bot - coderintuition.com")

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)
    print("New posting:", posting)

    return True


@tasks.loop(minutes=1.0)
async def fetch_postings():
    data = [line.decode("utf-8").strip() for line in urlopen(DATA_URL)]

    while HEADER_SEPARATOR not in data[0]:
        del data[0]
    del data[0]

    for row in data:
        row = [x.strip() for x in row.split('|')][1:-1]
        company_link = row[0].split('](')

        posting = {
            "company": company_link[0][1:],
            "link": company_link[1][:-1],
            "location": row[1] if len(row) > 1 else "",
            "status": row[2] if len(row) > 2 else "",
            "notes": row[3] if len(row) > 3 else "",
            "term": TERM
        }
        sent_posting = await send_posting(posting)

        if sent_posting: break  # only send one posting per loop to avoid spam


keep_alive()
my_secret = os.environ["TOKEN"]
client.run(my_secret)
