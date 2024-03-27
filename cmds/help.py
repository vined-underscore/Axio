import discord
import random
from discord.ext import commands
from util.embedder import Embedder
from util.colors import Colors as C
from discord.ext.commands import (
    Context,
    Cog
)
from axio import (
    Axio
)
from util.errors import AxioException


class Help(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    async def display_categories(
            self, ctx: Context,
            color: int
    ) -> None:
        await ctx.message.delete()
        commands = [command for command in self.bot.get_cog("Help").get_commands()]
        desc = ""
        em = discord.Embed(
            title=f"Categories",
            color=color
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        em.set_author(name=f"Axio v{self.bot.version} | {len(self.bot.commands)} Commands", url=None)
        em.set_thumbnail(
            url="https://media.discordapp.net/attachments/1139901136128721009/1212184056452620308/V5OzrAD.png?ex=65f0e960&is=65de7460&hm=eaa8cd1dc4e436caa7a3e181229df8b84686c4201c6240e792a70b13f1535df2&=&format=webp&quality=lossless")
        for command in commands:
            desc += f"{ctx.prefix}{command.name}: {command.description or command.brief or command.short_doc}\n"

        em.description = desc
        link = await Embedder.get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")

    async def display_commands(
            self, ctx: Context,
            cog: Cog,
            color: int,
            page: int
    ) -> None:
        commands = [command for command in cog.get_commands()]
        desc = f"'{ctx.prefix}{ctx.command.name} (page)' to see other commands\n\n"
        em = discord.Embed(
            title=f"{cog.qualified_name} Commands",
            color=color
        )
        provider = f"{self.bot.author['name']} ({self.bot.author['id']})"
        commands_per_page = 4

        index = [0, commands_per_page]
        if not (page - 1) * commands_per_page > len(commands):
            if (page - 1) < 0:
                index = [0, commands_per_page]
            else:
                index[0] += (page - 1) * commands_per_page
                index[1] += (page - 1) * commands_per_page

        current_page = (index[0] // commands_per_page) + 1
        total_pages = (len(commands) + commands_per_page - 1) // commands_per_page
        em.set_author(name=f"Axio v{self.bot.version} | Page {current_page}/{total_pages}", url=None)
        em.set_thumbnail(url=self.bot.em_thumbnail)
        for command in commands[index[0]:index[1]]:
            desc += f"{ctx.prefix}{command.name}: {command.description or command.brief or command.short_doc}\n\n"

        em.description = desc
        link = await Embedder.get_embed_link(em, provider)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="help",
        description="Displays the Axio categories",
        aliases=["cmds"]
    )
    async def help(self, ctx: Context):
        await self.display_categories(ctx, random.choice(C.BOT_COLORS))

    @commands.command(
        name="gethelp",
        description="Get the help info of a command",
        aliases=["cmd"]
    )
    async def gethelp(self, ctx: Context, command: str):
        cmd = self.bot.get_command(command)
        if not cmd:
            raise AxioException(f"Invalid command \"{command}\"{C.RESET}")

        link = await self.bot.command_help_link(ctx, cmd)
        await ctx.send(
            f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
        await ctx.message.delete()

    @commands.command(
        name="raid",
        description="Displays the raid commands"
    )
    async def raid(self, ctx: Context, page: int = 1):
        await self.display_commands(ctx, self.bot.get_cog("Raid"), random.choice(C.BOT_COLORS), page)

    @commands.command(
        name="fun",
        description="Displays the fun commands"
    )
    async def fun(self, ctx: Context, page: int = 1):
        await self.display_commands(ctx, self.bot.get_cog("Fun"), random.choice(C.BOT_COLORS), page)

    @commands.command(
        name="utility",
        description="Displays the utility commands"
    )
    async def utility(self, ctx: Context, page: int = 1):
        await self.display_commands(ctx, self.bot.get_cog("Utility"), random.choice(C.BOT_COLORS), page)

    @commands.command(
        name="dev",
        description="Displays the dev commands"
    )
    async def dev(self, ctx: Context, page: int = 1):
        await self.display_commands(ctx, self.bot.get_cog("Dev"), random.choice(C.BOT_COLORS), page)


async def setup(bot: Axio):
    await bot.add_cog(Help(bot))
