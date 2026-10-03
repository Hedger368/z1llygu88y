import os
import discord
from random import randint
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="z!", intents=intents)

def z1ll1fy(m3zz4g3):
    z1ll1f13d = ""
    r4nd0m_numb3rr = randint(1, 10)
    match r4nd0m_numb3rr:
        case 1:
            fl41r = ":3"
        case 2:
            fl41r = ":p"
        case 3:
            fl41r = ">_<"
        case 4:
            fl41r = "^_^"
        case 5:
            fl41r = ">:3"
        case 6:
            fl41r = "XP"
        case 7:
            fl41r = "X3"
        case 8:
            fl41r = ">:P"
        case 9:
            fl41r = ":P"
        case 10:
            fl41r = ">:p"
    for i in range(len(m3zz4g3)):
        ch4r4ct3rr = m3zz4g3[i].lower()
        match ch4r4ct3rr:
            case "a":
                ch4r4ct3rr = "4"
            case "e":
                ch4r4ct3rr = "3"
            case "i":
                ch4r4ct3rr = "1"
            case "o":
                ch4r4ct3rr = "0"
            case "s":
                ch4r4ct3rr = "z"
            case ".":
                ch4r4ct3rr = "!!"
            case "!":
                ch4r4ct3rr = "!!!!"
        z1ll1f13d = z1ll1f13d + ch4r4ct3rr
    z1ll1f13d = z1ll1f13d + " " + fl41r
    return(z1ll1f13d)

@bot.command()
async def trans(msg):
    if msg.message.reference and msg.message.reference.message_id:
        try:
            replied_message = await msg.channel.fetch_message(msg.message.reference.message_id)
            z1llyt3xt = z1ll1fy(str(replied_message.content))
            await msg.reply(z1llyt3xt)
        except discord.NotFound:
            print("d3l3t3d...")
        except discord.HTTPException:
            print("f41l3d t0 f3tch m3zz4g3...")
    else:
        await msg.reply("y0u d1dn't r3ply t0 4nyth1ng... :p")


bot.run(TOKEN)