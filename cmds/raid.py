import discord
import asyncio
import random
from colorama import Fore as F
from util.checks import guild_only, group_only
from itertools import cycle
from typing import Optional
from discord.ext.commands import Context
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord import Forbidden
from aiohttp import ClientSession
from axio import (
    Axio
)
from util.errors import AxioException


class Raid(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.command(
        name="stopspam",
        description="Stops any type of spam going on",
        aliases=["stops", "stopsp"]
    )
    async def stopspam(self, ctx: Context):
        await ctx.message.delete()
        self.bot.is_spamming = False
        try:
            await self.bot.spam_message.delete()
        except:
            pass

    @commands.command(
        name="spam",
        description="Spams a message in the current channel"
    )
    async def spam(self, ctx: Context, amount: Optional[int], *, msg: str):
        if self.bot.is_spamming:
            return await ctx.message.delete()

        await self.start_spam(
            ctx,
            ctx.channel,
            msg,
            amount,
            False
        )

    @commands.command(
        name="spamchannel",
        description="Spams a message in the specified channel (ID)",
        aliases=["spamc", "cspam"]
    )
    async def spamchannel(self, ctx: Context, channel_id: int, amount: Optional[int], *, msg: str):
        if self.bot.is_spamming:
            return await ctx.message.delete()
        if not channel_id:
            return await ctx.message.delete()

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return await ctx.message.delete()

        await self.start_spam(
            ctx,
            channel,
            msg,
            amount,
            False
        )

    @commands.command(
        name="spamall",
        description="Spams a message in all channels in the current guild",
        aliases=["aspam"]
    )
    @guild_only()
    async def spamall(self, ctx: Context, amount: Optional[int], *, msg: str):
        if self.bot.is_spamming:
            return await ctx.message.delete()

        await self.start_spamall(
            ctx,
            msg,
            amount,
            False
        )

    @commands.command(
        name="ghostspam",
        description="Spams and deletes a message in the current channel",
        aliases=["gspam"]
    )
    async def ghostspam(self, ctx: Context, amount: Optional[int], *, msg: str):
        if self.bot.is_spamming:
            return await ctx.message.delete()

        await self.start_spam(
            ctx,
            ctx.channel,
            msg,
            amount,
            True
        )

    @commands.command(
        name="ghostspamchannel",
        description="Spams and deletes a message in the specified channel (ID)",
        aliases=["gspamc"]
    )
    async def ghostspamchannel(self, ctx: Context, channel_id: int, amount: Optional[int], *, msg: str):
        if self.bot.is_spamming:
            return await ctx.message.delete()
        if not channel_id:
            return await ctx.message.delete()

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return await ctx.message.delete()

        await self.start_spam(
            ctx,
            channel,
            msg,
            amount,
            True
        )

    @commands.command(
        name="spamweb",
        description=f"Creates a webhook and spams it. Surround the name with \"\"",
        aliases=["spamw", "sweb"]
    )
    @guild_only()
    @commands.has_guild_permissions(manage_webhooks=True)
    async def spamweb(self, ctx: Context, amount: Optional[int], name: str = "Axio", *, message: str):
        self.bot.is_spamming = True

        await ctx.message.add_reaction("❌")
        webhook = await ctx.channel.create_webhook(name=name, reason="Axio")
        await self.start_spam(
            ctx,
            webhook,
            message,
            amount,
            False
        )

        await webhook.delete(reason="Axio")

    @commands.command(
        name="ghostspamall",
        description="Spams and deletes a message in all channels in the current guild",
        aliases=["gaspam", "gspamall"]
    )
    @guild_only()
    async def ghostspamall(self, ctx: Context, amount: Optional[int], *, msg: str):
        if self.bot.is_spamming:
            return await ctx.message.delete()

        await self.start_spamall(
            ctx,
            msg,
            amount,
            True
        )

    @commands.command(
        name="fastspam",
        description="Very fast inconsistent spam. Cannot be stopped"
    )
    async def fastspam(self, ctx: Context, amount: int = 20, *, msg: str):
        if amount > 50:
            raise AxioException("Amount cannot be higher than 50")

        ratelimits = []
        tasks = [self.send_http(ctx, msg, ratelimits) for _ in range(amount)]
        await asyncio.gather(*tasks)
        await ctx.message.delete()

    @commands.command(
        name="channelcreate",
        description="Creates an amount text channels in the current server",
        aliases=["ccr", "cc"]
    )
    @guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def channelcreate(self, ctx: Context, amount: int, *, name: str):
        if self.bot.is_channel_spamming:
            return

        self.bot.is_channel_spamming = True
        for _ in range(amount):
            if not self.bot.is_channel_spamming:
                break

            try:
                await ctx.guild.create_text_channel(name=name, reason="Axio")
            except:
                pass

        self.bot.is_channel_spamming = False
        await ctx.message.delete()

    @commands.command(
        name="channeldelete",
        description="Deletes all channels in the current server. Cannot be stopped",
        aliases=["cd"]
    )
    @guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def channeldelete(self, ctx: Context, name: str = None):
        if name:
            tasks = [channel.delete(reason="Axio") for channel in ctx.guild.channels if channel.name == name]
        else:
            tasks = [channel.delete(reason="Axio") for channel in ctx.guild.channels]

        await asyncio.gather(*tasks)
        await ctx.message.delete()

    @commands.command(
        name="rolecreate",
        description="Creates an amount of roles in the current server",
        aliases=["rc"]
    )
    @guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def rolecreate(self, ctx: Context, amount: int, *, name: str):
        if self.bot.is_role_spamming:
            return

        colors = cycle([
            (255, 215, 0),
            (12, 4, 4)
        ])

        self.bot.is_role_spamming = True
        for _ in range(amount):
            if not self.bot.is_role_spamming:
                break

            c = next(colors)
            try:
                await ctx.guild.create_role(name=name, color=discord.Color.from_rgb(c[0], c[1], c[2]), reason="Axio")
            except:
                pass

        self.bot.is_role_spamming = False
        await ctx.message.delete()

    @commands.command(
        name="roledelete",
        description="Deletes all roles in the current server. Cannot be stopped",
        aliases=["rd"]
    )
    @guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def roledelete(self, ctx: Context, *, name: str = None):
        if name:
            roles = [role for role in ctx.guild.roles[1:] if
                     role.name == name and not role.is_bot_managed() and role.is_assignable()]
        else:
            roles = [role for role in ctx.guild.roles[1:] if not role.is_bot_managed() and role.is_assignable()]

        tasks = [role.delete(reason="Axio") for role in roles]
        await asyncio.gather(*tasks)
        await ctx.message.delete()

    @commands.command(
        name="banall",
        description="Bans everyone in the current server"
    )
    @guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def banall(self, ctx: Context):
        if self.bot.is_banning:
            return

        self.bot.is_banning = True
        for member in ctx.guild.members:
            if not self.bot.is_banning:
                break

            if member.top_role.position >= ctx.guild.me.top_role.position:
                continue

            try:
                await member.ban(reason="Axio")
            except:
                pass

        self.bot.is_banning = False
        await ctx.message.delete()

    @commands.command(
        name="unbanall",
        description="Unbans everyone that is banned from the current server"
    )
    @guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unbanall(self, ctx: Context):
        if self.bot.is_banning:
            return

        self.bot.is_banning = True
        async for ban in ctx.guild.bans():
            if not self.bot.is_banning:
                break

            try:
                await ctx.guild.unban(ban.user, reason="Axio")
            except:
                pass

        self.bot.is_banning = False
        await ctx.message.delete()

    @commands.command(
        name="gcname",
        description="Spams the groupchat name an amount of times"
    )
    @group_only()
    async def gcname(self, ctx: Context, amount: int, *, text: str):
        self.bot.is_spamming_gc = True
        for i in range(amount):
            if not self.bot.is_spamming_gc:
                break

            await ctx.channel.edit(name=f"{text} {i + 1}")

        self.bot.is_spamming_gc = False
        await ctx.message.delete()

    @commands.command(
        name="massmention",
        description="Mentions every person in the current server (or specified channel)"
    )
    async def massmention(self, ctx: Context, channel_id: Optional[int], do_spam: Optional[bool]):
        channel_id = channel_id or ctx.channel.id
        channel = self.bot.get_channel(channel_id)
        print(do_spam)
        if not channel:
            return await ctx.message.delete()

        if not isinstance(channel, discord.abc.GuildChannel):
            return await ctx.message.delete()

        if isinstance(channel, discord.ForumChannel) \
                or isinstance(channel, discord.CategoryChannel) \
                or isinstance(channel, discord.StageChannel):
            return await ctx.message.delete()

        guild = channel.guild
        await guild.fetch_members(
            [discord.Object(ch.id) for ch in guild.channels],
            force_scraping=True
        )
        members = [
            member.mention for member in guild.members
            if not member.bot
            and member.id != self.bot.user.id
        ]
        pages = []

        for i in range(0, len(members), 10):
            chunk = members[i:i + 10]
            pages.append(chunk)

        self.bot.is_massmentioning = True
        if not do_spam:
            for p in pages:
                if not self.bot.is_massmentioning:
                    break

                try:
                    await channel.send(" ".join(p))
                except discord.Forbidden:
                    self.bot.is_massmentioning = False
        else:
            pages = cycle(pages)
            while self.bot.is_massmentioning:
                try:
                    await channel.send(" ".join(next(pages)))
                except discord.Forbidden:
                    self.bot.is_massmentioning = False

        await ctx.message.delete()
        self.bot.is_massmentioning = False

    async def start_spam(
            self,
            ctx: Context,
            send_to: discord.abc.Messageable | discord.Webhook,
            msg: str,
            amount: Optional[int],
            ghost: bool = False
    ):
        self.bot.is_spamming = True
        await ctx.message.add_reaction("❌")
        if amount:
            if amount >= 9999:
                return await ctx.message.delete()

            for _ in range(amount):
                if not self.bot.is_spamming:
                    break

                try:
                    if ghost:
                        if isinstance(send_to, discord.Webhook):
                            await send_to.send(msg, delete_after=0)
                        else:
                            await send_to.send(msg, delete_after=0)
                    else:
                        await send_to.send(msg)
                except MissingPermissions:
                    pass
                except Forbidden:
                    pass

            return await ctx.message.remove_reaction("❌", member=self.bot.user)
        else:
            while self.bot.is_spamming:
                try:
                    if ghost:
                        await send_to.send(msg, delete_after=0)
                    else:
                        await send_to.send(msg)
                except MissingPermissions:
                    pass
                except Forbidden:
                    pass

    @commands.command(
        name="nuke",
        description="Nukes the specified server. Using it too much will slow down the next nukes"
    )
    @guild_only()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx: Context, guild_id: int):
        if self.bot.is_nuking:
            return await ctx.message.delete()

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.message.delete()

        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Starting nuke in server {F.CYAN}{guild}")
        self.bot.is_nuking = True

        try:
            await guild.default_role.edit(permissions=discord.Permissions.all())
            print(
                f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Gave {F.GREEN}@everyone{F.LIGHTBLACK_EX} all permissions in {F.CYAN}{guild}")
        except:
            print(
                f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to give {F.RED}@everyone{F.LIGHTBLACK_EX} all permissions in {F.CYAN}{guild}")

        async for ban in guild.bans():
            if not self.bot.is_nuking:
                return

            try:
                await ctx.guild.unban(ban.user, reason="Axio")
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Unbanned {F.GREEN}{ban.user}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")
            except:
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to unban {F.RED}{ban.user}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")

        for member in guild.members:
            if not self.bot.is_nuking:
                return

            if member.top_role.position >= guild.me.top_role.position:
                continue

            try:
                await member.ban(reason="Axio")
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Banned {F.GREEN}{member}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")
            except:
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to ban {F.RED}{member}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")

        for role in guild.roles[1:]:
            if not self.bot.is_nuking:
                return

            if role.position >= guild.me.top_role.position:
                continue

            try:
                await role.delete(reason="Axio")
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Deleted role {F.GREEN}{role}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")
            except:
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to deleted role {F.RED}{role}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")

        for channel in guild.channels:
            if not self.bot.is_nuking:
                return

            try:
                await channel.delete(reason="Axio")
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Deleted channel {F.GREEN}{channel}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")
            except:
                print(
                    f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to deleted channel {F.RED}{channel}{F.LIGHTBLACK_EX} in {F.CYAN}{guild}")

        try:
            await guild.edit(
                name=self.bot.cfg["nuke"]["server_name"].replace("{servername}", guild.name),
            )
            print(
                f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Changed server name from {F.CYAN}{guild}{F.LIGHTBLACK_EX} to {F.GREEN}{self.bot.cfg['nuke']['server_name'].replace('{servername}', guild.name)}")
        except:
            print(
                f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to change server name from {F.CYAN}{guild}{F.LIGHTBLACK_EX} to {F.RED}{self.bot.cfg['nuke']['server_name'].replace('{servername}', guild.name)}")

        try:
            inv_channel = await guild.create_text_channel(name="ｎｕｋｅｄ－ｂｙ－ａｘｉｏ", reason="Axio", position=0)
            # sys_flags = discord.SystemChannelFlags()
            # sys_flags.join_notifications = True
            # sys_flags.join_notification_replies = True
            # await guild.edit(
            #     community=True,
            #     rules_channel=inv_channel,
            #     public_updates_channel=inv_channel,
            #     invites_disabled=False,
            #     system_channel=inv_channel,
            #     system_channel_flags=sys_flags,
            #     preferred_locale=discord.Locale.chinese
            # )
            invite = await inv_channel.create_invite(validate=None)
            print(f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Made invite {F.GREEN}{invite}")
        except Exception as e:
            print(
                f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Failed to make invite: {F.RED}{e}")

        for _ in range(499):
            if not self.bot.is_nuking:
                return

            try:
                channel = await guild.create_text_channel(name=random.choice(self.bot.cfg["nuke"]["channel_names"]),
                                                          reason="Axio")
                try:
                    webhook = await channel.create_webhook(name=random.choice(self.bot.cfg["nuke"]["webhook_names"]),
                                                           reason="Axio")
                    asyncio.create_task(
                        self.spam_webhook(
                            webhook,
                            random.choice(self.bot.cfg["nuke"]["webhook_names"]),
                            random.choice(self.bot.cfg["nuke"]["webhook_messages"])))
                except:
                    pass
            except:
                pass

        self.bot.is_nuking = False

    async def start_spamall(
            self,
            ctx: Context,
            msg: str,
            amount: Optional[int],
            ghost: bool = False
    ):
        self.bot.is_spamming = True
        await ctx.message.add_reaction("❌")
        if amount:
            if amount >= 9999:
                return await ctx.message.delete()

            for channel in ctx.guild.text_channels:
                for _ in range(amount):
                    if not self.bot.is_spamming:
                        break

                    try:
                        if ghost:
                            await channel.send(msg, delete_after=0)
                        else:
                            await channel.send(msg)
                    except MissingPermissions:
                        pass
                    except Forbidden:
                        pass

            return await ctx.message.remove_reaction("❌", member=self.bot.user)
        else:
            while self.bot.is_spamming:
                for channel in ctx.guild.text_channels:
                    try:
                        if ghost:
                            await channel.send(msg, delete_after=0)
                        else:
                            await channel.send(msg)
                    except MissingPermissions:
                        pass
                    except Forbidden:
                        pass

    async def send_http(self, ctx: Context, msg: str, ratelimits: list) -> None:
        async with ClientSession() as client:
            async with client.post(
                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                    headers={"Authorization": self.bot.http.token},
                    json={
                        "content": msg,
                        "tts": False
                    }
            ) as r:
                if r.status == 429:
                    data = await r.json()
                    await asyncio.sleep(float(data["retry_after"] + float(random.uniform(0.2, 1.5))))
                    if ratelimits:
                        ratelimits.append(self.send_http(ctx, msg, []))

    async def spam_webhook(self, webhook: discord.Webhook, name: str, message: str):
        while self.bot.is_nuking:
            try:
                await webhook.send(username=name, content=message)
            except:
                pass


async def setup(bot: Axio):
    await bot.add_cog(Raid(bot))
