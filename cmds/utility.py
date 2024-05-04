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
from util.token import get_token_data
from util.colors import Colors as C
from util.embed import get_embed_link
from util.errors import AxioException, InvalidToken
from discord.flags import UserFlags
from discord.ext.commands import (
    BadArgument
)

import requests
import whois
import time
import socket
from scapy.all import IP, ICMP, sr1
import shutil

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
        guild = self.bot.get_guild(guild_id) or ctx.guild
        if not guild:
            raise AxioException("Guild does not exist.")

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
        name="group",
        description="Get information about the current (or specified) group chat",
        aliases=["groupinfo"]
    )
    async def group(self, ctx: Context, channel_id: Optional[int]):
        group = self.bot.get_channel(channel_id) or ctx.channel
        if not isinstance(group, discord.GroupChannel):
            raise AxioException(f"{channel_id}: Not a group chat.")

        now = datetime.now().astimezone()
        created_at = group.created_at
        days_ago = now - created_at
        owner = self.bot.get_user(group.owner_id)
        owner_name = owner.name if owner else "No Owner"
        info = f"""{group.name} ({group.id})

Created At: {created_at.strftime("%b %d %Y")} ({days_ago.days} days ago)
Owner: {owner_name} ({group.owner_id})
Member Count: {len(group.recipients)}
Icon: {group.icon.url if group.icon else 'None'}"""
        em = discord.Embed(
            title="Group Information",
            description=info,
            color=random.choice(C.BOT_COLORS)
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version}", url=None)
        link = await get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()
        save_data(f"{self.bot.data_path}/groups/{group.name} {group.id}.txt", info)

    @commands.command(
        name="tokeninfo",
        description="Get information about an account token",
        aliases=["tinfo", "tokinfo"]
    )
    async def tokeninfo(self, ctx: Context, token: str):
        check = await get_token_data(token)
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

            await ctx.message.edit(content=f"""```ansi
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
    async def purge(self, ctx: Context, amount: int, channel_id: Optional[int]):
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
        description="Changes the accounts status (online, offline, dnd, idle)"
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
        description="Updates the accounts config without restarting the bot",
        aliases=["updatecfg"]
    )
    async def updatecfg(self, ctx: Context):
        self.bot.update_config()
        await ctx.message.delete()

    @commands.command(
        name="firstmsg",
        description="Sends the first message in the current (or specified) channel",
        aliases=["fmsg"]
    )
    async def firstmsg(self, ctx: Context, channel_id: Optional[int]):
        channel = self.bot.get_channel(channel_id) or ctx.channel
        msg = None
        async for message in channel.history(limit=1, oldest_first=True):
            msg = message

        if not msg:
            return await ctx.message.delete()
        else:
            await ctx.message.edit(content=msg.jump_url)

    @commands.command(
        name="prefixes",
        description="List all prefixes for the accounts config"
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
        description="Adds a prefix to the accounts config"
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
        description="Removes a prefix from the accounts config",
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
        description="Shows all logged deleted messages in the current (or specified) channel"
    )
    async def snipe(self, ctx: Context, channel_id: Optional[int]):
        channel = self.bot.get_channel(channel_id) or ctx.channel
        messages = self.bot.snipe_dict.get(channel.id)
        if not messages:
            return await ctx.message.delete()

        full = f"|--- Axio ---|\n\n- {channel.name} -\n\n\n"
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
        description="Shows the last edited message in the current (or specified) channel",
        aliases=["esnipe"]
    )
    async def editsnipe(self, ctx: Context, channel_id: Optional[int]):
        channel = self.bot.get_channel(channel_id) or ctx.channel
        sniped = self.bot.edit_snipe_dict.get(channel.id)
        if not sniped:
            return await ctx.message.delete()

        before = sniped["before"]
        after = sniped["after"]
        pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleanb = pattern.sub("", before.content.replace("`", ""))
        cleana = pattern.sub("", after.content.replace("`", ""))
        await ctx.message.edit(
            content=f"```ansi\n{C.YELLOW}{before.author} {C.RESET}| {C.YELLOW}{before.created_at}\n{C.LIGHT_BLUE}Before: {C.RESET}{cleanb}\n{C.LIGHT_BLUE}After: {C.RESET}{cleana}```")
    
    @commands.command(
        name="mac",
        description="Searches for MAC address info then displays it",
        aliases=["macaddress"]
    )
    async def mac(self, ctx: commands.Context, mac_address: str):
        macapi_url = f'https://api.maclookup.app/v2/macs/{mac_address}'
        try:
            response = requests.get(macapi_url)
            response.raise_for_status()
            data = response.json()
            if 'found' in data and data['found']:
                company = data.get('company', 'N/A')
                address = data.get('address', 'N/A')
                block_start = data.get('blockStart', 'N/A')
                block_end = data.get('blockEnd', 'N/A')
                block_size = data.get('blockSize', 'N/A')
                block_type = data.get('blockType', 'N/A')
                last_updated = data.get('updated', 'N/A')
                is_randomized = data.get('isRand', 'N/A')
                is_private = data.get('isPrivate', 'N/A')
                await ctx.message.edit(content=f"""```ansi\n{C.YELLOW}MAC Address Information{C.RESET}
                                       
- Company: {C.YELLOW}{company}{C.RESET}
- Address: {C.YELLOW}{address}{C.RESET}
- Block Start: {C.YELLOW}{block_start}{C.RESET}
- Block End: {C.YELLOW}{block_end}{C.RESET}
- Block Size: {C.YELLOW}{block_size}{C.RESET}
- Block Type: {C.YELLOW}{block_type}{C.RESET}
- Last Updated: {C.YELLOW}{last_updated}{C.RESET}
- Randomized: {C.YELLOW}{is_randomized}{C.RESET}
- Private: {C.YELLOW}{is_private}{C.RESET}```""")
            else:
                await ctx.message.edit(content=f"```ansi\n{C.RED}Vendor information not found for MAC Address: {mac_address}{C.RESET}```")
        except requests.exceptions.HTTPError as errh:
            await ctx.message.edit(content=f"```ansi\n{C.RED}HTTP Error: {errh}{C.RESET}```")
        except requests.exceptions.ConnectionError as errc:
            await ctx.message.edit(content=f"```ansi\n{C.RED}Error Connecting: {errc}{C.RESET}```")
        except requests.exceptions.Timeout as errt:
            await ctx.message.edit(content=f"```ansi\n{C.RED}Timeout Error: {errt}{C.RESET}```")
        except requests.exceptions.RequestException as err:
            await ctx.message.edit(content=f"```ansi\n{C.RED}An unexpected error occurred: {err}{C.RESET}```")
            
    @commands.command(
        name="minecraft",
        description="Searches for a minecraft username and displays any info about it",
        aliases=["uuid"]
    )
    async def minecraft(self, ctx: commands.Context, username_input: str):
        base_url = "https://api.mojang.com/users/profiles/minecraft/{}"
        history_url = "https://api.ashcon.app/mojang/v2/user/{}/names"
        skin_url = "https://crafatar.com/skins/{}"

        uuid_response = requests.get(base_url.format(username_input))
        if uuid_response.status_code == 200:
            uuid_data = uuid_response.json()
            uuid = uuid_data["id"]
            
            history_response = requests.get(history_url.format(uuid))
            if history_response.status_code == 200:
                history_data = history_response.json()
                previous_usernames = [entry["name"] for entry in history_data["names"]] if history_data.get("names") else []
                
                skin_url = skin_url.format(uuid)

                await ctx.message.edit(content=f"""```ansi\nUUID Info for {C.YELLOW}{username_input}{C.RESET}
                                       
- UUID: {C.YELLOW}{uuid}{C.RESET}
- Previous Usernames: {C.YELLOW}{', '.join(previous_usernames) if previous_usernames else 'N/A'}{C.RESET}
- Skin URL: {C.YELLOW}{skin_url}{C.RESET}```""")
            else:
                await ctx.message.edit(content=f"```ansi\n{C.RED}Failed to retrieve username history.{C.RESET}```")
        else:
            await ctx.message.edit(content=f"```ansi\n{C.RED}Failed to retrieve UUID.{C.RESET}```")
            
    @commands.command(
        name="whois",
        description="Perform a WHOIS lookup on a domain",
        aliases=["domain"]
    )
    async def whois(self, ctx: commands.Context, domain: str):
        try:
            result = whois.whois(domain)
            await ctx.message.edit(content=f"""```ansi\n Domain info for: {C.YELLOW}{domain}{C.RESET}
                                   
- Registrar: {C.YELLOW}{result.registrar}{C.RESET}
- Creation Date: {C.YELLOW}{result.creation_date}{C.RESET}
- Expiration Date: {C.YELLOW}{result.expiration_date}{C.RESET}
- Name Servers: {C.YELLOW}{', '.join(result.name_servers)}{C.RESET}
- Registrant: {C.YELLOW}{result.registrant}{C.RESET}
- Admin Contact: {C.YELLOW}{result.admin}{C.RESET}
- Tech Contact: {C.YELLOW}{result.tech}{C.RESET}

Domain owners info
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
- Name: {C.YELLOW}{result.name}{C.RESET}
- State / Area: {C.YELLOW}{result.state}{C.RESET}
- Owners address: {C.YELLOW}{result.address}{C.RESET}
- Phone number: {C.YELLOW}{result.phone}{C.RESET}
- Email address: {C.YELLOW}{result.email}{C.RESET}```""")
        except whois.parser.PywhoisError as e:
            await ctx.message.edit(content=f"```ansi\n{C.RED}Error: {e}{C.RESET}```")
            
    @commands.command(
        name="wafbypass",
        description="Perform WAF bypass on a target URL",
        aliases=["waf"]
    )
    async def wafbypass(self, ctx: commands.Context, url: str, bypass_ssl: bool = False):
        # Load payloads from JSON file
        payloads_file_path = os.path.join("configs", "payloads.json")
        with open(payloads_file_path) as f:
            payloads_data = json.load(f)
            common_payloads = payloads_data.get("payloads", [])

        results = []

        for payload in common_payloads:
            headers = {'User-Agent': payload}

            try:
                if bypass_ssl:
                    response = requests.get(url, headers=headers, verify=False)
                else:
                    response = requests.get(url, headers=headers)
                
                results.append({
                    'payload': payload,
                    'status_code': response.status_code,
                    'response_content': response.text
                })

            except requests.exceptions.SSLError as ssl_error:
                results.append({
                    'payload': payload,
                    'ssl_error': str(ssl_error)
                })
        
        output = ""
        for result in results:
            output += f"+ Payload: {result['payload']}\n"
            if 'status_code' in result:
                output += f"- Status Code: {result['status_code']}\n"
            elif 'ssl_error' in result:
                output += f"- SSL Verification Error: {result['ssl_error']}\n"
            output += "\n"

        os.makedirs("outputs", exist_ok=True)

        output_file_path = os.path.join("outputs", "WAFbypass_output.txt")
        with open(output_file_path, "w") as file:
            file.write(output)

        with open(output_file_path, "rb") as file:
            message = await ctx.send(file=discord.File(file, filename="WAFbypass_output.txt"))
            await ctx.message.edit(content=f"```ansi\n{C.YELLOW}Attempting to bypass via payloads{C.RESET}```")
        shutil.rmtree("outputs")
            
    @commands.command(
        name="traceroute",
        description="Perform a traceroute to a target",
        aliases=["trace"]
    )
    async def traceroute(self, ctx: commands.Context, target: str): #Really annoying lol
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            await ctx.message.edit(content=f"```ansi\n{C.RED}Invalid target address.{C.RESET}```")
            return

        result = f"```ansi\nTraceroute to {target} ({C.YELLOW}{target_ip}{C.RESET}):```\n```ansi\n"
        result += "{:<5} {:<20} {:<20} {:<10}\n".format("Hop", "IP Address", "ICMP Type", "RTT (ms)")

        for ttl in range(1, 31):
            packet = IP(dst=target_ip, ttl=ttl) / ICMP()
            start_time = time.time()
            reply = sr1(packet, verbose=0, timeout=1)
            end_time = time.time()
            if reply is None:
                break
            if reply.type == 0:
                result += f"{ttl:<5} {reply.src:<20} {C.YELLOW}[Reached destination]{C.RESET}"
                break
            else:
                rtt_ms = (end_time - start_time) * 1000
                icmp_type = reply[ICMP].type if reply.haslayer(ICMP) else ""
                result += "{:<5} {:<20} {:<20} {:.2f} ms\n".format(ttl, get_info(reply), icmp_type, rtt_ms)

        result += "```"
        await ctx.message.edit(result)
def get_info(reply):
    info = ""
    if reply.haslayer(IP):
        info += f"{reply[IP].src}"
    return info

async def setup(bot: Axio):
    await bot.add_cog(Utility(bot))
