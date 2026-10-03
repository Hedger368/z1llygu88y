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

@bot.command()
async def sing(msg):
    song = msg.message.content[7:].strip().lower()
    print(song)
    match song:
        case "verity":
            lyrics = """h3y, 1t'z m3, 1t'z v3r1ty!! ^_^
4zk m3 4nyth1ng!!! :3
1 kn0w, 4b0ut, 4 m1ll10n th1ngz!! >:3
1'll d0 4nyth1ng!!!! XP"""
        case "misery":
            lyrics = """1 m1zz th4t k1nd 0f m1z3ry :3
d4 k1nd wh3r3 y0u w3r3 n1c3 t0 m3h T_T
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! :p"""
        case "backrooms":
            lyrics = """v3r1ty'z fr0m m1n3cr4ft!!! >:3
h3 b3l0ngz t0 b4ckr00mz!!!! >_<"""
        case "gubby":
            """gu88y d1z, gu88y d4t! :3
gubb3h s3rv3r, gubb3h l4n!! ^_^
gubb3h w1f1, gubb3h r4m :p
gubb3h zt34k, gubb3h h4m!! X3
az14n gubb3h fr0m j4p4n, n0w 1'm gubb1n w1th my fr13ndz!! >_<
4ll d4 gubb13z g01ng h444m!!!!! X3"""
        case _:
            lyrics = "z0rry, 1 d0n't kn0w th4t z0ng... O_o"
    await msg.reply(lyrics)

bot.run(TOKEN)