import os
import discord
import asyncio
from discord.ext import commands
from colorama import Fore as F
from axio import Axio


def get_channel_name(channel: discord.abc.MessageableChannel) -> str:
    if isinstance(channel, discord.TextChannel) \
            or isinstance(channel, discord.VoiceChannel) \
            or isinstance(channel, discord.ForumChannel):
        return f"#{channel.name} in {channel.guild.name}"
    elif isinstance(channel, discord.DMChannel):
        return f"@{channel.recipient.name}"
    else:
        return channel.name


class Events(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        if not self.bot.is_main:
            self.bot.has_printed_stats = True
            return

        os.system("cls" if os.name == "nt" else "clear")
        os.system("title Axio")
        await self.bot.banner()

        # try:
        #     if self.bot.cfg["plugins"]["axiocmd"]:
        #         self.bot.axiocmd = AxioCMD(self.bot, Terminal())
        #         await self.bot.axiocmd.menu()
        # except Exception as error:
        #     traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if int(payload.user_id) == int(self.bot.user.id) and payload.emoji.name == "❌":
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(msg)
            if ctx.command:
                self.bot.spam_message = msg

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if int(payload.user_id) == int(self.bot.user.id):
            if payload.emoji.name == "❌":
                self.bot.is_spamming = False

                channel = self.bot.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                print(f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Stopped spamming{F.RESET}")
                await asyncio.sleep(2)
                await msg.delete()
            # elif payload.emoji.name == "⏸️" and payload.message_id == self.bot.animating["message"]["id"]:
            #     channel = self.bot.get_channel(payload.channel_id)
            #     msg = await channel.fetch_message(payload.message_id)     
            #     if msg.reactions == []:
            #         return

            #     self.bot.animating["is_animating"] = not self.bot.animating["is_animating"]
            #     await msg.add_reaction("⏸️")
            #     if self.bot.animating["is_animating"]:
            #         name = self.bot.animating["name"]
            #         show_info = self.bot.animating["show_info"]
            #         with open("./data/animate/animations.json", "r") as f:
            #             data = json.load(f)

            #         for idx, frame in enumerate(data[name]["frames"][self.bot.animating["frame_index"] + 1::]):
            #             if not self.bot.animating["is_animating"]:
            #                 break

            #             self.bot.animating["frame_index"] = idx + self.bot.animating["frame_index"] # Frame counter after pausing is broken
            #             print(self.bot.animating)
            #             info = f"Animation **{name}** | Frame **{idx}/{len(data[name]["frames"]) - 1}**\n\n"
            #             await msg.edit(f"""{info if show_info else ""}{frame}""")
            #             await asyncio.sleep(data[name]["delay"])

            # elif payload.emoji.name == "⏹️" and payload.message_id == self.bot.animating["message"]["id"]:
            #     self.bot.animating["is_animating"] = False
            #     channel = self.bot.get_channel(payload.channel_id)
            #     msg = await channel.fetch_message(payload.message_id)
            #     for reaction in msg.reactions:
            #         if reaction.me:
            #             await reaction.remove(self.bot.user)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        self.bot.messages_count += 1
        if message.author.id in self.bot.copycat_ids:
            try:
                if message.content.startswith(tuple(self.bot.command_prefix)):
                    return
            except Exception as e:
                print(e)

            try:
                await message.channel.send(message.content)
            except:
                pass

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.bot.snipe_dict[message.channel.id] = message

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        self.bot.edit_snipe_dict[before.channel.id] = {
            "before": before,
            "after": after
        }
        await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if not self.bot.can_log("bot_joined_server"):
            return

        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Joined server {F.GREEN}{guild} ({guild.id}){F.RESET}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        if not self.bot.can_log("bot_left_server"):
            return

        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Left server {F.RED}{guild} ({guild.id}){F.RESET}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not self.bot.can_log("member_joined"):
            return

        guild = member.guild
        user = member._user
        if user == self.bot.user:
            return

        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}{user} {F.LIGHTBLACK_EX}joined server {F.GREEN}{guild} ({guild.id}){F.RESET}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if not self.bot.can_log("member_left"):
            return

        guild = member.guild
        user = member._user
        if user == self.bot.user:
            return

        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}{user} {F.LIGHTBLACK_EX}left server {F.RED}{guild} ({guild.id}){F.RESET}")

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if not self.bot.can_log("commands"):
            return

        command = ctx.command
        if not self.bot.has_printed_stats:
            return

        if command.name == "eval":
            return

        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Executed command {F.YELLOW}{command.name}{F.LIGHTBLACK_EX} at {F.CYAN}{get_channel_name(ctx.channel)}")


async def setup(bot: Axio):
    await bot.add_cog(Events(bot))
