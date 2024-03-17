import re
import traceback
import aiohttp
import discord
import sys
from axio import Axio
from time import perf_counter
from discord.ext import commands
from colorama import Fore as F

class NitroSniper(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not self.bot.cfg["nitro_sniper"]["enabled"]:
            return
        
        regex = re.compile("(discord.gift/|discord.com/gifts/|discordapp.com/gifts/)([a-zA-Z0-9]+)")
        if regex.search(msg.content):
            if self.bot.cfg["nitro_sniper"]["ignore_self"] and msg.author == self.bot.user:
                return
            code = regex.search(msg.content).group(2)
            try:
                request = await self.claim_nitro(msg, code)
                self.log_console(code, request["message"], request["delay"], msg)
                await self.log_claim(code, request["message"], request["delay"], msg)
            except Exception as error:
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def claim_nitro(
        self, msg: discord.Message,
        code: str
    ) -> dict:
        start = perf_counter()
        async with aiohttp.ClientSession() as client:
            async with await client.post(
                f"https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem",
                json={
                    "channel_id": str(msg.channel.id)
                }, headers={
                    "Authorization": self.bot.http.token
                }) as r:
                    end = perf_counter()
                    data = await r.json()
                    return {
                        "message": data["message"],
                        "delay": end - start,
                        "status_code": r.status
                    }
           
    def status_color(self, status: str) -> tuple[discord.Color, int]:
        if "This gift has been redeemed already" in status\
            or "Unknown Gift Code" in status:
            return (discord.Color(0xff434b), F.RED)
        elif "nitro" in status:
            return (discord.Color(0xB59410), F.GREEN)
        else:
            return (discord.Color.dark_gray(), F.BLACK)
             
    async def log_claim(
        self, code: str,
        status: str,
        delay: float,
        msg: discord.Message
    ) -> None:
        if self.bot.nitro_hook:
            async with aiohttp.ClientSession() as client:
                self.bot.nitro_hook.session = client
                color = self.status_color(status)[0]
                try:
                    em = discord.Embed(
                        title="Axio Sniper",
                        color=color
                    )
                    em.set_thumbnail(url=self.bot.em_thumbnail)
                    em.add_field(name="Location", value=f"""
Channel: **{self.get_channel_name(msg.channel)}** {msg.channel.jump_url}
User: **{msg.author.mention}** ({msg.author.id})""", inline=False)
                    em.add_field(name="Claim Status", value=f"**{status}**", inline=False)
                    em.add_field(name="Code", value=f"https://discord.gift/{code}", inline=False)
                    em.add_field(name="Delay", value=f"**{'%.3fs' % delay}**", inline=False)
                    ping_everyone = self.bot.cfg["nitro_sniper"]["webhook"]["ping_everyone"]
                    await self.bot.nitro_hook.send(
                        content="@everyone" if ping_everyone else None,
                        embed=em,
                        username="Axio",
                        avatar_url=self.bot.em_thumbnail
                    )
                except Exception as error:
                    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    def log_console(
        self, code: str,
        status: str,
        delay: float,
        msg: discord.Message
    ) -> None:
        color = self.status_color(status)[1]
        print(f"""
{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.YELLOW}Sniped{F.LIGHTBLACK_EX} a possible nitro code
{F.WHITE}|{F.LIGHTBLACK_EX} Status: {color}{status}{F.LIGHTBLACK_EX}
{F.WHITE}|{F.LIGHTBLACK_EX} Code: {F.YELLOW}{code}{F.LIGHTBLACK_EX}
{F.WHITE}|{F.LIGHTBLACK_EX} Delay: {F.YELLOW}{'%.3fs' % delay}{F.LIGHTBLACK_EX}
{F.WHITE}|{F.LIGHTBLACK_EX} {F.YELLOW}{self.get_channel_name(msg.channel)}{F.RESET}\n""")
        
    def get_channel_name(self, channel: discord.abc.Messageable) -> str:
        if isinstance(channel, discord.TextChannel)\
        or isinstance(channel, discord.VoiceChannel)\
        or isinstance(channel, discord.ForumChannel):
            return f"#{channel.name} in {channel.guild.name}"
        elif isinstance(channel, discord.DMChannel):
            return f"@{channel.recipient.name}"
        else:
            return channel.name

async def setup(bot: Axio):
    await bot.add_cog(NitroSniper(bot))