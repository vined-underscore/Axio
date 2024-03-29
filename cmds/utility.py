import base64
import json
import discord
import random
import os
import re
import aiohttp
from io import StringIO
from os import PathLike
from axio import Axio
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Context
from util.token import check_token
from util.colors import Colors as C
from util.embedder import get_embed_link
from util.errors import AxioException, InvalidToken
from discord.flags import UserFlags
from discord.ext.commands import (
    BadArgument
)


def save_data(
        path: str | PathLike | Path,
        data: Any
):
    with open(path, "w+") as f:
        f.write(data)


class Utility(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.command(
        name="stop",
        description="Stops every action occurring in the bot"
    )
    async def stop(self, ctx: Context):
        await self.bot.clear_actions()
        await ctx.message.delete()

    @commands.command(
        name="cls",
        description="Clears the console",
        aliases=["clearconsole"]
    )
    async def cls(self, ctx: Context):
        os.system("cls" if os.name == "nt" else "clear")
        os.system("title Axio")
        await self.bot.banner()
        await ctx.message.delete()

    @commands.command(
        name="user",
        description="Get information about your profile (or the specified user)",
        aliases=["userinfo"]
    )
    async def user(self, ctx: Context, user: Optional[discord.User]):
        if not user:
            user = ctx.author

        now = datetime.now().astimezone()
        created_at = user.created_at
        days_ago = now - created_at
        info = f"""{user.name} ({user.id})

Created At: {created_at.strftime("%b %d %Y")} ({days_ago.days} days ago)
Bot: {user.bot}
Flags: {user.public_flags.value}
Avatar: {user.avatar.url if user.avatar else 'None'}"""
        em = discord.Embed(
            title="User Information",
            description=info,
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_thumbnail(url=user.avatar.with_size(64).url)
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()
        save_data(f"{self.bot.data_path}/users/{user.name} {user.id}.txt", info)

    @commands.command(
        name="server",
        description="Get information about the current (or specified) server",
        aliases=["serverinfo"]
    )
    async def server(self, ctx: Context, guild_id: Optional[int]):
        if not guild_id:
            if not ctx.guild:
                return await ctx.message.delete()

            guild_id = ctx.guild.id

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.message.delete()

        now = datetime.now().astimezone()
        created_at = guild.created_at
        days_ago = now - created_at
        owner = await guild.fetch_member(guild.owner_id)
        owner_name = owner.name if owner else "No Owner"
        info = f"""{guild.name} ({guild.id})

Created At: {created_at.strftime("%b %d %Y")} ({days_ago.days} days ago)
Owner: {owner_name} ({guild.owner_id})
Member Count: {guild.member_count}
Channel Count: {len(guild.channels)}
Role Count: {len(guild.roles)}
Icon: {guild.icon.url if guild.icon else 'None'}"""
        em = discord.Embed(
            title="Server Information",
            description=info,
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()
        save_data(f"{self.bot.data_path}/servers/{guild.name} {guild.id}.txt", info)

    @commands.command(
        name="tokeninfo",
        description="Get information about an account token",
        aliases=["tinfo", "tokinfo"]
    )
    async def tokeninfo(self, ctx: Context, token: str):
        check = await check_token(token)
        if not check[0]:
            raise InvalidToken()

        data = check[1]
        mfa = "Yes" if data['mfa_enabled'] else "No"
        user_flags = {val.value: name for name, val in UserFlags.__members__.items()}
        info = f"""{data['username']} ({data['id']})

Email: {data['email']}
Phone: {data['phone']}
2FA: {mfa}
Flags: {user_flags.get(data['flags'])} ({data['flags']})
"""
        em = discord.Embed(
            title="Token Information",
            description=info,
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()
        save_data(f"{self.bot.data_path}/tokens/{data['username']} {data['id']}.txt", info)

    @commands.command(
        name="geoip",
        description="Get information about an IP address",
        aliases=["ipinfo"]
    )
    async def geoip(self, ctx: Context, ip: str):
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"http://ip-api.com/json/{ip}")
            r_ = await client.get(f"https://ipinfo.io/widget/demo/{ip}")
            data = await r.json()
            data_ = await r_.json()
            if data["status"] == "fail":
                return await ctx.message.delete()

            await ctx.message.edit(f"""```ansi
{C.YELLOW}{ip}{C.RESET} Information

- Country: {C.YELLOW}{data['country']}{C.RESET}
- Country Code: {C.YELLOW}{data['countryCode']}{C.RESET}
- Region Name: {C.YELLOW}{data['regionName']}{C.RESET}
- City: {C.YELLOW}{data['city']}{C.RESET}
- Zip Code: {C.YELLOW}{data['zip']}{C.RESET}
- Latitude: {C.YELLOW}{data['lat']}{C.RESET}
- Longitude: {C.YELLOW}{data['lon']}{C.RESET}
- Timezone: {C.YELLOW}{data['timezone']}{C.RESET}
- ISP: {C.YELLOW}{data['isp']}{C.RESET}
- Hostname: {C.YELLOW}{data_['data']['hostname']}{C.RESET}
- Org: {C.YELLOW}{data['org'] if data['org'] else None}{C.RESET}
- AS: {C.YELLOW}{data['as'] if data['as'] else None}{C.RESET}
- VPN: {C.YELLOW}{data_['data']['privacy']['vpn']}{C.RESET}
- Proxy: {C.YELLOW}{data_['data']['privacy']['proxy']}{C.RESET}
- Tor: {C.YELLOW}{data_['data']['privacy']['tor']}{C.RESET}```""")

    @commands.command(
        name="friends",
        description="Saves all your friends in the accounts data path"
    )
    async def friends(self, ctx: Context):
        friend_list = [user.user for user in self.bot.friends]
        with open(f"{self.bot.data_path}/friends/friends.json", "w+") as f:
            data = {}
            for friend in friend_list:
                data[friend.id] = {
                    "username": friend.name,
                    "user_id": friend.id,
                    "created_at": friend.created_at.strftime("%d/%m/%Y, %H:%M:%S")
                }
                if friend.discriminator != "0":
                    data[friend.id]["discriminator"] = friend.discriminator

            json.dump(data, f, indent=4)

        await ctx.message.delete()

    @commands.command(
        name="purge",
        description="Purges an amount of messages from you in the current (or specified) channel",
        aliases=["clear"]
    )
    async def purge(self, ctx: Context, amount: int, channel_id: int = None):
        channel = self.bot.get_channel(channel_id) or ctx.channel
        if not channel:
            raise BadArgument("You either don't have access to the specified channel or it doesn't exist.")

        await ctx.message.delete()
        self.bot.is_purging = True
        if isinstance(channel, discord.GroupChannel) or isinstance(channel, discord.DMChannel):
            async for message in channel.history(limit=amount):
                if not self.bot.is_purging:
                    return
                if not message.author == self.bot.user:
                    continue
                if message == ctx.message:
                    continue

                await message.delete()
        else:
            def purge(m):
                return m.author == self.bot.user and m != ctx.message

            await channel.purge(limit=amount, check=purge, reason="Axio")
            self.bot.is_purging = False

    @commands.command(
        name="botstats",
        description="Shows bot statistics"
    )
    async def botstats(self, ctx: Context):
        em = discord.Embed(
            title="Bot Statistics",
            description=f"""
Latency: {round(self.bot.latency * 1000)}ms
Uptime: {self.bot.get_uptime()}
Cached Messages: {self.bot.messages_count}
Cached Users: {len(self.bot.users)}
Servers: {len(self.bot.guilds)}""",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="status",
        description="Changes the bot status (online, offline, dnd, idle)"
    )
    async def status(self, ctx: Context, status: str):
        match status:
            case "online":
                await self.bot.change_presence(
                    status=discord.Status.online
                )
            case "offline":
                await self.bot.change_presence(
                    status=discord.Status.offline
                )
            case "dnd":
                await self.bot.change_presence(
                    status=discord.Status.dnd
                )
            case "idle":
                await self.bot.change_presence(
                    status=discord.Status.idle
                )
            case _:
                raise AxioException(
                    f"{C.RED}Invalid status. Must be one of these: {C.YELLOW}online, offline, dnd, idle{C.RESET}")

        await ctx.message.delete()

    @commands.command(
        name="playing",
        description="Starts a playing activity on your account"
    )
    async def playing(self, ctx: Context, *, text: str):
        await self.bot.change_presence(
            status=self.bot.status,
            activity=discord.Game(name=text)
        )
        await ctx.message.delete()

    @commands.command(
        name="watching",
        description="Starts a watching activity on your account"
    )
    async def watching(self, ctx: Context, *, text: str):
        await self.bot.change_presence(
            status=self.bot.status,
            activity=discord.Activity(type=discord.ActivityType.watching, name=text)
        )
        await ctx.message.delete()

    @commands.command(
        name="listening",
        description="Starts a listening activity on your account"
    )
    async def listening(self, ctx: Context, *, text: str):
        await self.bot.change_presence(
            status=self.bot.status,
            activity=discord.Activity(type=discord.ActivityType.listening, name=text)
        )
        await ctx.message.delete()

    @commands.command(
        name="streaming",
        description="Starts a streaming activity on your account"
    )
    async def streaming(self, ctx: Context, *, text: str):
        await self.bot.change_presence(
            status=self.bot.status,
            activity=discord.Streaming(name=text, url="https://youtube.com")
        )
        await ctx.message.delete()

    @commands.command(
        name="clearactivity",
        description="Clears your current activity"
    )
    async def clearactivity(self, ctx: Context):
        await self.bot.change_presence(
            status=self.bot.status,
            activity=None
        )
        await ctx.message.delete()

    @commands.command(
        name="updateconfig",
        description="Updates the config without restarting the bot. Doesn't work with the token",
        aliases=["updatecfg"]
    )
    async def updatecfg(self, ctx: Context):
        self.bot.update_config()
        await ctx.message.delete()

    @commands.command(
        name="firstmsg",
        description="Sends the first message in the current channel",
        aliases=["fmsg"]
    )
    async def firstmsg(self, ctx: Context):
        msg = None
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            msg = message

        if not msg:
            return await ctx.message.delete()
        else:
            await ctx.message.edit(content=msg.jump_url)

        await ctx.message.delete()

    @commands.command(
        name="prefixes",
        description="List all prefixes in the bot"
    )
    async def prefixes(self, ctx: Context):
        prefix = self.bot.command_prefix
        nl = "\n"
        em = discord.Embed(
            title=f"{len(prefix)} Prefixes",
            description=f"{nl.join([f'{idx + 1}. {p}' for idx, p in enumerate(prefix)])}",
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="addprefix",
        description="Adds a prefix to the bot"
    )
    async def addprefix(self, ctx: Context, prefix: str):
        if len(prefix) > 32:
            raise AxioException(f"{C.RED}Prefix cannot be longer than 32 characters")

        with open(self.bot.cfg_path, "r+") as f:
            data = json.load(f)
            if prefix in data["prefixes"]:
                raise AxioException(f"{C.RED}Prefix already exists")

            data["prefixes"].append(prefix)
            with open(self.bot.cfg_path, "w+") as out:
                json.dump(data, out, indent=4)

        self.bot.command_prefix.append(prefix)
        await ctx.message.delete()

    @commands.command(
        name="removeprefix",
        description="Removes a prefix from the bot",
        aliases=["delprefix"]
    )
    async def removeprefix(self, ctx: Context, prefix: str):
        with open(self.bot.cfg_path, "r+") as f:
            data = json.load(f)
            if prefix not in data["prefixes"]:
                raise AxioException(f"{C.RED}Prefix doesn't exist")

            data["prefixes"].remove(prefix)
            with open(self.bot.cfg_path, "w+") as out:
                json.dump(data, out, indent=4)

        self.bot.command_prefix.remove(prefix)
        await ctx.message.delete()

    @commands.command(
        name="encodeb64",
        descriptions="Encodes a string to base64",
        aliases=["eb64"]
    )
    async def encodeb64(self, ctx: Context, *, string: str):
        try:
            encoded = base64.b64encode(string.encode("ascii")).decode("ascii")
            await ctx.message.edit(content=f"```\n{encoded}```")
        except UnicodeEncodeError:
            raise AxioException("Invalid characters")

    @commands.command(
        name="decodeb64",
        descriptions="Decodes base64 to a string",
        aliases=["db64"]
    )
    async def decodeb64(self, ctx: Context, *, string: str):
        try:
            decoded = base64.b64decode((string + "==").encode("ascii")).decode("ascii")
            await ctx.message.edit(content=f"```\n{decoded}```")
        except UnicodeDecodeError:
            raise AxioException("Invalid base64 string")

    @commands.command(
        name="reverse",
        description="Reverses a string",
        aliases=["flip"]
    )
    async def reverse(self, ctx: Context, *, string: str):
        await ctx.message.edit(content=f"```\n{string[::-1]}```")

    @commands.command(
        name="snipe",
        description="Shows all logged deleted messages in the current channel"
    )
    async def snipe(self, ctx: Context):
        messages = self.bot.snipe_dict.get(ctx.channel.id)
        full = "|--- Axio ---|\n\n"
        for message in messages:
            nl = "\n"
            full += f"{message.author.name} | {message.created_at}\n    {message.content}\n{nl.join([att.url for att in message.attachments])}\n"

        file = StringIO(full)
        await ctx.message.delete()
        await ctx.send(file=discord.File(file, filename=f"{len(messages)}-Deleted-Messages.txt"))

    @commands.command(
        name="clearsnipe",
        description="Clears the deleted message list"
    )
    async def clearsnipe(self, ctx: Context):
        self.bot.snipe_dict[ctx.channel.id] = []
        await ctx.message.delete()

    @commands.command(
        name="editsnipe",
        description="Shows the last edited message in the current channel",
        aliases=["esnipe"]
    )
    async def editsnipe(self, ctx: Context):
        sniped = self.bot.edit_snipe_dict.get(ctx.channel.id)
        if not sniped:
            return await ctx.message.delete()

        before = sniped["before"]
        after = sniped["after"]
        pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleanb = pattern.sub("", before.content.replace("`", ""))
        cleana = pattern.sub("", after.content.replace("`", ""))
        await ctx.message.edit(
            content=f"```ansi\n{C.YELLOW}{before.author} {C.RESET}| {C.YELLOW}{before.created_at}\n{C.LIGHT_BLUE}Before: {C.RESET}{cleanb}\n{C.LIGHT_BLUE}After: {C.RESET}{cleana}```")


async def setup(bot: Axio):
    await bot.add_cog(Utility(bot))
