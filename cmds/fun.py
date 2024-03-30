import asyncio
import discord
import json
import base64
import socket
import struct
import random
import string
from art import text2art
from util.colors import Colors as C
from axio import Axio
from util.embedder import get_embed_link
from typing import Optional
from discord.ext import commands
from discord.ext.commands import Context


class Fun(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.command(
        name="token",
        description="(doesn't) Token grab someone",
        aliases=["tokengrab"]
    )
    async def token(self, ctx: Context, user: discord.User):
        with open(f"{self.bot.data_path}/fun/fake_tokens.json") as json_f:
            data = json.load(json_f)

        em = discord.Embed(
            title="Token Grab",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)

        user_id = str(user.id)
        if user_id not in data:
            id_ascii = user_id.encode("ascii")
            id_base64 = base64.b64encode(id_ascii)
            id_idk = id_base64.decode("ascii").replace("==", "")
            timest = "".join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=6))
            last = "".join(random.choices(string.ascii_letters + string.digits + "-" + "_", k=27))
            em.description = f"Token grabbed @{user.name}.\nToken: {id_idk}.{timest}.{last}"
            data[user_id] = f"{id_idk}.{timest}.{last}"

            with open(f"{self.bot.data_path}/fun/fake_tokens.json", "w") as out:
                json.dump(data, out, indent=4)

        else:
            token = data[user_id]
            em.description = f"Token grabbed @{user.name}.\nToken: {token}"

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="ip",
        description="(doesn't) IP grab someone",
        aliases=["ipgrab"]
    )
    async def ip(self, ctx: Context, user: discord.User):
        with open(f"{self.bot.data_path}/fun/fake_ips.json") as json_f:
            data = json.load(json_f)

        em = discord.Embed(
            title="IP Grab",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        user_id = str(user.id)

        if user_id not in data:
            rand_ip = socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xffffffff)))
            em.description = f"IP grabbed {user.name}.\nIP Address: {rand_ip}"
            data[user_id] = rand_ip

            with open(f"{self.bot.data_path}/fun/fake_ips.json", "w") as out:
                json.dump(data, out, indent=4)

        else:
            ip = data[user_id]
            em.description = f"IP grabbed {user.name}.\nIP Address: {ip}"

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="copycat",
        description="Copies every message sent by an user. Can be used with multiple users",
        aliases=["copy"]
    )
    async def copycat(self, ctx: Context, user: discord.User):
        em = discord.Embed(
            title="Copycat",
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)

        if user.id == self.bot.user.id:
            em.colour = discord.Color.red()
            em.description = "You can't copy yourself"
            link = await get_embed_link(em, provider)
            return await ctx.send(
                f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")

        if user.id in self.bot.copycat_ids:
            self.bot.copycat_ids.remove(user.id)
            em.colour = random.choice(C.BOT_COLORS)
            em.description = f"Stopped copying @{user.name}"
            link = await get_embed_link(em, provider)
            await ctx.send(
                f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")

        else:
            self.bot.copycat_ids.append(user.id)
            em.colour = random.choice(C.BOT_COLORS)
            em.description = f"Started copying @{user.name}"
            link = await get_embed_link(em, provider)
            await ctx.send(
                f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")

        await ctx.message.delete()

    @commands.command(
        name="copycatclear",
        description="Clears the list of copycat users",
        aliases=["copyclear"]
    )
    async def copycatclear(self, ctx: Context):
        self.bot.copycat_ids = []
        await ctx.message.delete()

    @commands.command(
        name="animate",
        description="Starts an animation. Add \"yes\" or \"no\" before the name to show info like frame index"
    )
    async def animate(self, ctx: Context, show_info: str = "no", *, name: str):
        em = discord.Embed(
            title="Animate",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
            data = json.load(f)
            if not data.get(name):
                em.description = f"Animation with name {name} does not exist"
            else:
                self.bot.animating["is_animating"] = True
                self.bot.animating["name"] = name
                self.bot.animating["message"]["id"] = ctx.message.id
                self.bot.animating["message"]["channel_id"] = ctx.message.channel.id
                self.bot.animating["show_info"] = True if show_info == "yes" else False
                # await ctx.message.add_reaction("⏸️") # Frame counter after pausing is broken
                # await ctx.message.add_reaction("⏹️")
                for idx, frame in enumerate(data[name]["frames"]):
                    if not self.bot.animating["is_animating"]:
                        break

                    self.bot.animating["frame_index"] = idx
                    info = f"Animation **{name}** | Frame **{idx}/{len(data[name]['frames']) - 1}**\n\n"
                    await ctx.message.edit(content=f"""{info if show_info == "yes" else ""}{frame}""")
                    await asyncio.sleep(data[name]["delay"])

                # for reaction in ctx.message.reactions:
                #     if reaction.me:
                #         await reaction.remove(self.bot.user)

                return

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="animations",
        description="Lists all animation"
    )
    async def animations(self, ctx: Context, page: int = 1):
        with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
            data = json.load(f)

        animations = [anim for anim in data]
        desc = f"'{ctx.prefix}{ctx.command.name} (page)' to see other animations\n\n"
        em = discord.Embed(
            title="Animations",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        anims_per_page = 5

        index = [0, anims_per_page]
        if not (page - 1) * anims_per_page > len(animations):
            if (page - 1) < 0:
                index = [0, anims_per_page]
            else:
                index[0] += (page - 1) * anims_per_page
                index[1] += (page - 1) * anims_per_page

        current_page = (index[0] // anims_per_page) + 1
        total_pages = (len(animations) + anims_per_page - 1) // anims_per_page
        em.set_author(name=f"Axio v{self.bot.version} | Page {current_page}/{total_pages}", url=None)
        em.set_thumbnail(url=self.bot.em_thumbnail)
        for animation in animations[index[0]:index[1]]:
            anim = data[animation]
            desc += f"{animation} | {anim['delay']}s delay | {len(anim['frames'])} frames\n"

        em.description = desc
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="stopanimate",
        description="Stops the current ongoing animation",
        aliases=["stopanim"]
    )
    async def stopanimate(self, ctx: Context):
        self.bot.animating["is_animating"] = False
        await ctx.message.delete()

    @commands.command(
        name="createanimation",
        description="Creates an animation",
        aliases=["createanim"]
    )
    async def createanimation(self, ctx: Context, delay: Optional[float] = 1.0, *, name: str):
        em = discord.Embed(
            title="Create Animation",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        if delay < 0.5:
            em.description = "The delay cannot be lower than 0.5 seconds"
        elif len(name) > 32:
            em.description = "The name cannot be longer than 32 characters"
        else:
            with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
                data = json.load(f)
                if data.get(name):
                    em.description = f"Animation \"{name}\" already exists. You can delete it or change the frames by using {ctx.prefix}editframe"
                else:
                    data[name] = {
                        "delay": delay,
                        "frames": []
                    }
                    with open(f"{self.bot.data_path}/animate/animations.json", "w+") as out:
                        json.dump(data, out, indent=4)

                    em.description = f"Created animation with name \"{name}\". Each frame will have a {delay} second delay."

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="deleteanimation",
        description="Delete an animation",
        aliases=["delanim", "deleteanim"]
    )
    async def deleteanimation(self, ctx: Context, *, name: str):
        em = discord.Embed(
            title="Delete Animation",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
            data = json.load(f)
            if not data.get(name):
                em.description = f"The animation \"{name}\" does not exist"
            else:
                del data[name]
                with open(f"{self.bot.data_path}/animate/animations.json", "w+") as out:
                    json.dump(data, out, indent=4)

                em.description = f"Deleted animation with name \"{name}\""

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="addframe",
        description="Adds a frame to an animation. Surround the animation name with \"\""
    )
    async def addframe(self, ctx: Context, name: str, index: Optional[int], *, text: str):
        em = discord.Embed(
            title="Add Frame",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
            data = json.load(f)
            if not data.get(name):
                em.description = f"Animation with name {name} does not exist"
            else:
                if index:
                    data[name]["frames"].insert(index, text)
                else:
                    data[name]["frames"].append(text)

                with open(f"{self.bot.data_path}/animate/animations.json", "w+") as out:
                    json.dump(data, out, indent=4)

                em.description = f"Added frame at index {index or len(data[name]['frames']) - 1} to animation \"{name}\""

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="deleteframe",
        description="Deletes a frame of an animation. Get the index by using the animate command",
        aliases=["delframe"]
    )
    async def deleteframe(self, ctx: Context, name: str, index: int):
        em = discord.Embed(
            title="Delete Frame",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
            data = json.load(f)
            if not data.get(name):
                em.description = f"Animation with name \"{name}\" does not exist"
            else:
                try:
                    data[name]["frames"][index]
                except:
                    em.description = f"Frame at index {index} does not exist"

                else:
                    del data[name]["frames"][index]
                    with open(f"{self.bot.data_path}/animate/animations.json", "w+") as out:
                        json.dump(data, out, indent=4)

                    em.description = f"Deleted frame at index {index} from animation \"{name}\""

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="editframe",
        description="Edits a frame of an animation. Get the index by using the animate command",
        alias=["modifyframe"]
    )
    async def editframe(self, ctx: Context, name: str, index: int, *, text: str):
        em = discord.Embed(
            title="Edit Frame",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        with open(f"{self.bot.data_path}/animate/animations.json", "r") as f:
            data = json.load(f)
            if not data.get(name):
                em.description = f"Animation with name \"{name}\" does not exist"
            else:
                try:
                    data[name]["frames"][index]
                except:
                    em.description = f"Frame at index {index} does not exist"

                else:
                    data[name]["frames"][index] = text
                    with open(f"{self.bot.data_path}/animate/animations.json", "w+") as out:
                        json.dump(data, out, indent=4)

                    em.description = f"Modified frame at index {index} from animation \"{name}\""

        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="ascii",
        description="Turns a string into ASCII art"
    )
    async def ascii(self, ctx: Context, *, string: str):
        wall = ""
        if len(string) > 8:
            split = []
            count = 0
            current = ""
            for char in string:
                if count < 8:
                    current += char
                    if char != " ":
                        count += 1
                else:
                    if current != " ":
                        count = 1
                        split.append(current)

                    current = char

            if current:
                split.append(current)

            for el in split:
                text = text2art(el)
                wall += f"```\n{text}```\n"
        else:
            text = text2art(string)
            wall = f"```\n{text}```"

        await ctx.message.edit(content=wall)


async def setup(bot: Axio):
    await bot.add_cog(Fun(bot))
