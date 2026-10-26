import os
import socket
import discord
from random import randint, choice
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

gubbycolour = 0xffa3f1

word_accepted_endings = [" ", ".", ":", ";", ",", "?", "!", "-", ")", '"', "'", "}", "]", "~", "=", "+"]
word_accepted_prefixes = [" ", "-", "~", "(", "[", "{", "=", "+", ]

ver = "z0.7.0"

class Help(commands.HelpCommand):
    def __init(self):
        super().__init__(command_attrs={"brief": "zh0wz d1z m3zz4g3!!!"})
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="c0mm4nd h3lp!!!", color=gubbycolour)
        for command in self.context.bot.commands:
            if command.hidden:
                continue
            embed.add_field(name="z!"+command.name, value=command.help or "n0 g1v3n d3zcr1pt10n...", inline=False)
        await self.context.message.reply(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name, description=command.help or "n0 g1v3n d3zcr1pt10n...", color=gubbycolour)
        await self.context.message.reply(embed=embed)

    async def send_cog_help(self, cog):
        return

    async def send_group_help(self, group):
        return

bot = commands.Bot(command_prefix="z!", intents=intents, help_command=Help())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}", flush=True)
    # Let systemd count a deployment as started only after Discord is ready.
    notify_socket = os.getenv("NOTIFY_SOCKET")
    if notify_socket:
        if notify_socket.startswith("@"):
            notify_socket = "\0" + notify_socket[1:]
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client:
            client.connect(notify_socket)
            client.sendall(b"READY=1")

def check_for_word(message, index, word, allow_s=False):
    message = message.lower()
    word = word.lower()
    is_seperate = True
    if index > len(message) - len(word):
        is_seperate = False
    if message[index:index+len(word)] == word:
        if index == len(message) - len(word):
            is_seperate = True
        elif message[index+len(word)] in word_accepted_endings:
            is_seperate = True
        elif allow_s and message[index+len(word)] == "s":
            if index == (len(message) - len(word)) - 1:
                is_seperate = True
            elif message[index+len(word)+1] in word_accepted_endings:
                is_seperate = True
            else:
                is_seperate = False
        else:
            is_seperate = False
    else:
        is_seperate = False
    if is_seperate:
        if index != 0:
            if message[index-1] not in word_accepted_prefixes:
                is_seperate = False
    return is_seperate

def get_song_name(message):
    song = ""
    for i in range(7, len(message)):
        if message[i] != "+":
            song = song + message[i]
        else:
            break
    return song.strip()

def z1ll1fy(m3zz4g3):
    z1ll1f13d = ""
    r4nd0m_numb3rr = randint(1, 15)
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
        case 11:
            r4nd0m_numb3rr_2 = randint(1, 4)
            match r4nd0m_numb3rr_2:
                case 1:
                    fl41r = "o_o"
                case 2:
                    fl41r = "o_O"
                case 3:
                    fl41r = "O_o"
                case 4:
                    fl41r = "O_O"
        case 12:
            fl41r = ";3"
        case 13:
            fl41r = "> ~ <"
        case 14:
            fl41r = "> - <"
        case 15:
            fl41r = "^ ~ ^"
        case 15:
            fl41r = "^ - ^"
    i = 0
    while i < len(m3zz4g3):
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
        if check_for_word(m3zz4g3, i, "to"):
            ch4r4ct3rr = "2"
            i += 1
        if check_for_word(m3zz4g3, i, "too"):
            ch4r4ct3rr = "2"
            i += 2
        if check_for_word(m3zz4g3, i, "the"):
            ch4r4ct3rr = "d4"
            i += 2
        if check_for_word(m3zz4g3, i, "gubby", True):
            ch4r4ct3rr = "gubb3h"
            i += 4
        if check_for_word(m3zz4g3, i, "that", True):
            ch4r4ct3rr = "d4t"
            i += 3
        if check_for_word(m3zz4g3, i, "this", True):
            ch4r4ct3rr = "d1z"
            i += 3
        if check_for_word(m3zz4g3, i, "baby", True):
            ch4r4ct3rr = "b3b3h"
            i += 3
        if check_for_word(m3zz4g3, i, "what", True):
            ch4r4ct3rr = "w4t"
            i += 3 
        if check_for_word(m3zz4g3, i, "me", True):
            ch4r4ct3rr = "m3h"
            i += 1           
        z1ll1f13d = z1ll1f13d + ch4r4ct3rr
        i += 1

    z1ll1f13d = z1ll1f13d + " " + fl41r
    return(z1ll1f13d)

@bot.command()
async def trans(msg):
    """1 w1ll tr4nzl4t3 n*rm4l t3xt 1nt0 z1lly t3xt!!"""
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
async def sing(msg, *args):
    """1 w1ll z1ng 4 z0ng f0r y0u!!!"""
    if len(args) == 0:
        await msg.reply("r3m3mb3r, z!sing g03z l1k3 z!sing + [z0ng] [v3rz3] 0r z!sing [z0ng]...")
        return
    if args[0] != "+":
        song = args[0:-1]
        verse = "random"
    else:
        song = " ".join(args[0:-2])
        verse = args[-1]
    match song:

        case "verity":

            if verse == "random":
                verse = choice(["chorus", "prechorus", "bridge", "verse1", "verse2"])
            
            match verse:
                case "chorus":
                    lyrics = """h3y, 1t'z m3h, 1t'z v3r1ty!! ^_^
4zk m3h 4nyth1ng!!! :3
1 kn0w, 4b0ut, 4 m1ll10n th1ngz!! >:3
1'll d0 4nyth1ng!!!! XP"""

                case "prechorus":
                    lyrics = """d0 y0u l1v3 4l0n3?? 1z 4nyb0dy h0m3??? :3
0n3 tw0 thr33 4nd z0, wh3r3 d1d 3v3ryb0dy g0???? o_O"""

                case "bridge":
                    lyrics = """c0m3... c0m3 cl0z3r... >:3
c0m3 b3 my fr13nd! d0nt b3 z0 zc4red! ^_^
L0V3 M3H!!! XP"""

                case "verse1":
                    lyrics = """wh4tz d4 c4pit4l 0f fr4nc3?? O_o
0h 0u1 0u1 0u1! 1t 1z p4r1z!! m3rc1!!!! :3
0k4y... wh4t d03z d4 c0w z4y???? ^ - ^
0h m00 m00 m00! 1 zp34k d4t t00! 4ll d4y!!! XP"""

                case "verse2":
                    lyrics = """whyz d4 d00r l0ck3d up z0 t1ght?? T_T
0h t33 h33 h33! n0 n33d t0 l34v3! st4y h3r3!!! >:3
why d0 y0u kn0w wh3r3 1 zl33p??? > ~ <
0h 1 juzt kn0w... 1 4lw4yz kn0w... 1m cl0z3!!! XD"""

                case _:
                    lyrics = """1 kn0w 4 l0t 0f v3r1tyz, but 1 d0n't kn0w d4t 0n3, z0rry..."""


        case "misery":

            if verse == "random":
                verse = choice(["chorus", "bridge", "verse1", "verse2", "chorus2", "chorus3", "chorus4"])

            match verse:

                case "chorus":
                    lyrics = """1 m1zz d4t k1nd 0f m1z3ry :3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h T_T
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! :p"""

                case "verse1":
                    lyrics = """1 l0v3 y0u z0 much d4t 1tz dr1pp1ng <3
dr1pp1ng fr0m my 4rmz 4nd zuch :3
1m z0rry 1 kn0w 1m t00 much T_T
t0 l0v3, t0 truzt, 1m n0th1ng but </3"""

                case "verse2":
                    lyrics = """y0u 4r3 wh4t 1 c0uld b3l13v3 1n z1nc3 1 h4v3 n0b0dy 3lz3 T-T
1 k33p zcr34m1ng, 1 k33p br34th1ng, 1tz d4 l1v1ng 1 c4nt h3lp > - <
1tz d4 m1z3ry d4t y0u c4n t3ll m3h h0w much d4t y0u c4r3 ^ - ^
4nd 1 kn0w 1tz tru3 but y3t y0u n33d t0 g3t m3h 0ut y0ur h41r XP
1z wh4t w3 h4v3 zp3c14l?? w4tz d4t m34n??? o_O
why c4nt y0u ch00z3 m3h?? 1z 1t gr33d??? T-T
d1z 1znt luzt, n0 f41ry duzt, 1tz blunt, 1tz wh4t y0u z33!! :3
m1z3ry 1n kn0w1ng 1 l0v3 y0u 4nd h4d t0 l34v3 </3
d4 m1z3ry d4t 1 c4nt zh4k3, d4 m1z3ry 1 bl33d... T-T"""

                case "bridge":
                    lyrics = """hurtz t0 f33l d4t k1nd 0f m1z3ry :3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h T_T
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! :p
h0w t0 h34l d4t k1nd 0f m1z3ry >:3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h </3
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! XP"""

                case "chorus2":
                    lyrics = """1 m1zz d4t k1nd 0f m1z3ry :3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h T_T
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! :p
but 1tz r34l, d4t k1nd 0f m1z3ry > ~ <
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h ;3
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! X3"""

                case "chorus3":
                    lyrics = """1 m1zz d4t k1nd 0f m1z3ry :3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h T-T
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! :p
g0d 1 f33l d4t k1nd 0f m1z3ry T-T
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h > - <
but 0nly 1n d4 3v3n1ng... why 0nly 1n d4 3v3n1ng??? o_O"""

                case "chorus4":
                    lyrics = """hurtz t0 f33l d4t k1nd 0f m1z3ry :3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h T_T
but 0nly 1n d4 3v3n1ng z0 1 4zk 4m 1 juzt dr34m1ng!! :p
h0w t0 h34l d4t k1nd 0f m1z3ry >:3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h </3
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h T-T
t0 h34l d4t k1nd 0f m1z3ry > - <
d4 k1nd wh3r3 y0u 4r3 n1c3 t0 m3h ;3
but 0nly 1n d4 3v3n1ng, z0 1 w1zh d4t 1 w4z dr34m1ng.. T-T
but 0nly 1n d4 3v3n1ng... </3
g0d, 1 w1zh d4t 1 w4z dr34m1ng... ^ - ^
1 m1zz d4t k1nd 0f m1z3ry... :3
"""

                case _:
                    lyrics = "1 m1zz d4t k1nd 0f m1z3ry, but 1 d0nt kn0w d4t k1nd 0f m1z3ry, z0rry..."


        case "backrooms":

            lyrics = """v3r1ty'z fr0m m1n3cr4ft!!! >:3
h3 b3l0ngz t0 b4ckr00mz!!!! >_<"""


        case "gubby":

            if verse == "random":
                verse = choice(["chorus", "verse"])

            match verse:

                case "chorus":
                    lyrics = """gubb3h d1z, gubb3h d4t! :3
gubb3h s3rv3r, gubb3h l4n!! >_<
gubb3h w1f1, gubb3h r4m :p
gubb3h zt34k, gubb3h h4m!! X3
4z14n gubb3h fr0m j4p4n, n0w 1'm gubb1n w1th my fr13ndz!! >:3
4ll d4 gubb13z g01ng h444m!!!!! X3"""

                case "verse":
                    lyrics = '''"4r3 y0u 0k4y?" y3z 1 4m!! 1m m4k1ng gubb3h z0ngz!!!! :3
l3tz d4nc3 w1th d4 b34t, 4nd r3p34t, d4 gubb3h z1ng 4l0ng!!! XP
1f y0u d0nt 4gr33, y0u c4n l34v3, 1 w0nt br1ng y0u 4l0ng!! > ~ <
d4tz why y0u c4n z33, 1ll d0 3v3ryth1ng f0r gubb3h n0w!!! :D'''

                case _:
                    lyrics = "1z d4t 4 gubb3h??? n0, z3r10uzly, 1 d0nt kn0w d4t 0n3, z0rry..."


        case "aura farmer":

            if verse == "random":
                verse = choice(["chorus", "prechorus", "verse1", "verse2", "bridge"])

            match verse:
                case "chorus":
                    lyrics = """d0, d0, d0- d0-d0-d0, d0, d0h, 4h!! :3
d4 4ur4 f4rm3h (m3h!!! :p)
d0, d0, d0- d0-d0-d0, d0h, d0h, 4h!!! o - O
h3'z zuch 4 ch4rm3h ^_^"""

                case "prechorus":
                    lyrics = """l00k z0 fr3zh, g0d 1n fl3zh, 3v3ryb0dy 4t my f33t!! ;3
zun l00kz d1m, n3xt t0 h1m, b4by f33l d4 h34t!!! XP"""

                case "verse1":
                    lyrics = """w4k3 up 1n d4 m0rn1ng, 1m f33l1ng n0 ztr3zz!! ^ _ ^
41nt g0t n0 w0rr13z, c4uz3 1 kn0w 1m d4 b3zt!! :p
n0t 3v3n try1ng, 1 w4z b0rn l1k3 d1z!!! X3
juzt f33l d4 4ur4, b4b3 g1v3 m3 4 k1zz!! <3"""

                case "verse2":
                    lyrics = '''p4p4 4lw4yz t0ld m3h, "y0ur 4ur4 1z g0n3!!!!" T-T
but th3n 1 r34l1z3d, 1 w4znt h1z z0n!! (1m 4 gubb3h :3)
4nd wh3n 1m d0wn, 1 r3v1v3 myz3lf!! :p
c4uz3 1n d4ng3r, n0b0dy c4n h3lp!!! X3'''

                case "bridge":
                    lyrics = """m4n... d03znt 1t zuck t0 b3 4l0n3?? ^ - ^
t0 b3 4 l0z3r... 1 gu3zz 1ll n3v3r kn0w!!! :3
F33L D4 ZUN!! (4ur4!) :D
F33L D4 W1ND!!! (f4rm4h!) > ~ <
F33L D4 BL00D 1N Y0UR V31NZ!!!!! (4ur4!) X3
F33L D4 AUR4!!!!!!!!! XP"""

                case _:
                    lyrics = "1 h4v3 4 l0t 0f 4ur4, but 3v3n 1 d0nt kn0w w4t d4t 1z, z0rry..."
                

        case "lord verity":

            if verse == "random":
                verse = choice(["chorus", "verse1", "verse2", "bridge"])

            match verse:
                case "chorus":
                    lyrics = """th3y c4ll m3h l0rd!!! v3r1t3h!! :D
m4zt3r 0f hum4n1t3h!! >:3
1 z41d l000rd!!! v3r1t3h!! ^_^
c4ll m3h m4zt3r, m4zt3r, 0w!!! > ~ <"""

                case "verse1":
                    lyrics = """kn33l, zt0p! > - <
1 w4nt d1z th1ng t0 n3v3r, n3v3r 3nd!! :3
n3v3r 3v3r 3nd, 4h! n3v3r 3v3r 3nd, 4h!! :p
w41t, dr0p! 1 w4nn4 b3 y0ur 0n3 4nd 0nly fr13nd!!! ^ _ ^
0n3 4nd 0nly fr13nd, 4h! 0n3 4nd 0nly fr13nd, 4h!! XP"""

                case "verse2":
                    lyrics = """h3ll, n0!! ;3
1 w1ll n0t 3v3r l3t y0u g0 4w4y!! > ~ <
n3v3r g0 4w4y, 4h! n3v3r g0 4w4y, 4h!! :p
n000w, y0u!! 4r3 tr4pp3d f0r3v3r, d1z 1z my d0m41n!! X3
tr4pp3d 1n my d0m41n, 4h! tr4pp3d 1n my d0m41n, 4h!! XP"""

                case "bridge":
                    lyrics = """4lr1ght, y0ur f1n4l ch4nc3... 4zk m3h 4nyth1ng... ^_^
-# Can I ever afford a house?
## N00000!!!!!! >:3
-# W-What day is it today?
## y0ur L4ZT!!!!!!! >;3
-# How old is Taylor Swift?
### 1 d0nt g1v3 4 d4mn, h4h4h4H4H4H4!!! >:P
l0rd, v3r1t3h! m4zt3r 0f hum4n1ty!! :p
1f th3z3 4r3 r34lly y0ur l4zt qu3zt10nz... y0u d0nt d3z3rv3 y0ur br41n at 4ll!!! X3"""

                case _:
                    lyrics = "1m 4 m4zt3r 0f 4 l0t 0f th1ngz, but n0t d1z, z0rry..."

        case "homer" | "homer let the barts out":

            if verse == "random":
                verse = choice(["chorus", "verse1", "chorus2", "outro"])

            match verse:

                case "chorus":
                    lyrics = """h0m3r l3t d4 b4rtz 0ut!! :3
h0m3r l3t d4 b4rtz 0ut!!!! > ~ <
h3 0p3n3d up d4 d00r (h3 0p3n3d up d4 d00r)!! :p
th3y st4rt3d runn1ng, th3y st4rt3d runn1ng!!! X3
h0m3r l3t d4 b4rtz 0ut! ;3"""

                case "verse1":
                    lyrics = """h3 z41d h3 h4d c0ntr0l!! ^ - ^
h3 z41d h3 h4d c0ntr0l!!! XP
h3 d1d n0t h4v3 c0ntr0l!! o_O
h3 d1d n0t h4v3 c0ntr0l!!!! > ~ <"""

                case "chorus2":
                    lyrics = """h0m3r l3t d4 b4rtz 0ut (4nd th3yr3 n3v3r c0m1ng b4ck!!) :3
h0m3r l3t d4 b4rtz 0ut (n0w th3y 4ll up 1n d4 tr4ck!!! :p)
h0m3r l3t d4 b4rtz 0ut (4nd h3 c4nt d0 n0th1ng n0w!! >:3)
h0m3r l3t d4 b4rtz 0ut (h0m3r t00k d4t l z0m3h0w!! ^_^)"""

                case "outro":
                    lyrics = """d4 d00r 1z 0p3n, d4 b4rtz 4r3 fr33!! > ~ <
h0m3r zt4nd1ng th3r3, 1n d1zb3l13f!!! XP"""

                case _:
                    lyrics = """h0m3r d03znt kn0w d4t v3rz3, z0rry..."""

        case _:
            lyrics = "z0rry, 1 d0n't kn0w d4t z0ng... O_o"
    await msg.reply(lyrics)

@bot.command()
async def pet(msg):
    """p3t m3h!!!!"""
    choice = randint(1, 13)
    match choice:
        case 1:
            reply = ":3"
        case 2:
            reply = "m3w :3"
        case 3:
            reply = "1 l1k3 g3tt1ng p3t ^_^"
        case 4:
            reply = "ny4h :3"
        case 5:
            reply = "th4nkz > ~ <"
        case 6:
            reply = "m30w :p"
        case 7:
            reply = "mrrp :3"
        case 8:
            reply = "m3w! >:3"
        case 9:
            reply = "th4nkz f0r d4 p3tz!! ^_^"
        case 10:
            reply = "my4h.. ;3"
        case 11:
            reply = "gubb3h l0v3z y0u!! <3 :D"
        case 12:
            reply = ":D"
        case 13:
            reply = "purrr :3"
    await msg.reply(reply)

@bot.command()
async def version(msg):
    """zhowz d4 curr3nt v3rz10n!!"""
    await msg.reply(f'curr3tly 0n v3rz10n {ver}, m3w! :3')

@bot.command()
async def changelog(msg, *args):
    """zh0wz d4 ch4ng3l0g f0r 4 g1v3n upd4t3!!!"""
    if len(msg.message.content) > 11:
        requested_version = msg.message.content[11:].strip().lower()
    else:
        requested_version = "gub"
    reply = f'ch4ng3l0g f0r upd4t3 {requested_version}:'
    match requested_version:
        case "z0.1.0":
            reply += "\n- r3l34z3d d4 gubb3h!!\n- 4dd3d z!trans"
        case "z0.2.0":
            reply += "\n- 4dd3d z!sing\n- f1x3d z!trans br34k1ng w1th 3ll1pz3z"
        case "z0.2.1":
            reply += "\n- 4dd3d gubb3h z0ng t0 z!sing"
        case "z0.2.2":
            reply += "\n- f1x3d gubb3h z0ng 1n z!sing"
        case "z0.2.3":
            reply += "\n- b4ck3nd ch4ng3z wh1ch 4ll0w f0r m0r3 fr3qu3nt upd4t3z"
        case "z0.3.0":
            reply += "\n- 4dd3d 1nd1r3ct w0rd tr4nzl4t10nz t0 z!trans\n- 4dd3d m0r3 3m0t1c0nz t0 z!trans :3"
        case "z0.3.1":
            reply += "\n- c0d3 ch4ng3z t0 z!trans wh1ch f1x3d 1nd1r3ct w0rd tr4nzl4t10nz\n- 4dd3d m0r3 1nd1r3ct w0rd tr4nzl4t10nz t0 z!sing\n- 4dd3d zupp0rt f0r plur4lz f0r 1nd1r3ct w0rd tr4nzl4t10nz"
        case "z0.3.2":
            reply += "\n- 4dd3d 4ur4 f4rm3r 4nd l0rd v3r1ty z0ngz t0 z!sing"
        case "z0.3.3":
            reply += "\n- f1x3d f0rm1tt1ng bug f0r 4ur4 f4rm3r z0ng 1n z!sing"
        case "z0.4.0":
            reply += "\n- 4dd3d z!p3t c0mm4nd"
        case "z0.5.0":
            reply += "\n- c0mpl3t3ly 0v3rh4ul3d z!sing, 4ll0w1ng f0r d1ff3r3nt v3rz3z\n- 4dd3d m0r3 1nd1r3ct w0rd tr4nzl4t10nz"
        case "z0.5.1":
            reply += "\n- f1x3d v3rz3 z3l3ct10n n0t w0rk1ng\n- f1x3d 1nv4l1d v3rz3 c4z3 f0r l0rd v3r1ty z0ng"
        case "z0.5.2":
            reply += "\n- f1x3d gubb3h z0ng ch00z1ng 1nv4l1d v3rz3 1nzt34d 0f v3rz3 1 1f v3rz3 w4znt pr0v1d3d"
        case "z0.5.3":
            reply += "\n- f1x3d z!trans 1nd1r3ct w0rd tr4nzl4t10nz wr0ngly 4ct1v4t1ng 1f w0rdz w3r3 pr3f1x3d"
        case "z0.6.0":
            reply += "\n- 4dd3d z!version\n- 4dd3d z!changelog"
        case "z0.6.1":
            reply += "\n- 4dd3d z!xomer"
        case "z0.7.0":
            reply += "\n- r3w0rk3d z!h3lp t0 m4k3 1t n0t d4 d3f4ult d1zc0rd b0t h3lp m3zz4g3\n- 4dd3d d3zcr1pt10nz t0 c0mm4ndz"
        case "z0.7.1":
            reply += "\n- 4dd3d h0m3r l3t d4 b4rtz 0ut z0ng t0 z!sing\n- 1mpr0v3d c0d3 f0r z!sing 4nd z!changelog"
        case _:
            reply = "1nv4l1d v3rz10n, z0rry..."
    await msg.reply(reply)

@bot.command(hidden=True)
async def xomer(msg):
    """z9xomer"""
    user_sent = msg.author.name
    if user_sent == "z9xomer":
        reply = "h3ll0 z9, m3w! :3"
    else:
        reply = "l4rp."
    await msg.reply(reply)

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set DISCORD_TOKEN in the environment or a .env file.")
    bot.run(TOKEN)
