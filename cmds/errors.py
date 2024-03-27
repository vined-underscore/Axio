from colorama import Fore as F
from discord.ext import commands
from discord.ext.commands import Context
from util.colors import Colors as C
from discord.ext.commands import (
    CommandNotFound,
    MissingRequiredArgument,
    BadArgument,
    MissingPermissions,
    CheckFailure,
    CheckAnyFailure
)
from axio import (
    Axio
)
from util.errors import AxioException


class Errors(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        if ctx.cog:
            if ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)
        if isinstance(error, CommandNotFound):
            return

        if isinstance(error, MissingRequiredArgument):
            link = await self.bot.command_help_link(ctx, ctx.command)
            await ctx.send(
                f"{self.bot.user.mention}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{link}")
            await ctx.message.delete()

        elif isinstance(error, BadArgument):
            await self.error(ctx, error,
                             f"```ansi\n{C.YELLOW}{ctx.clean_prefix}{ctx.command.qualified_name}{C.RESET}: {C.RED}You entered a parameter incorrectly.```")

        elif isinstance(error, MissingPermissions):
            await self.bot.clear_actions()
            perms = "\n".join([f"{C.YELLOW}{perm.title().replace('_', ' ')}" for perm in error.missing_permissions])
            await self.error(ctx, error,
                             f"```ansi\n{C.YELLOW}{ctx.clean_prefix}{ctx.command.qualified_name}{C.RESET}: {C.RED}You don't have enough permissions to run this command.\n{C.YELLOW}Permissions needed:\n{perms}```")

        elif isinstance(error, AxioException):
            await self.error(ctx, error,
                             f"```ansi\n{C.YELLOW}{ctx.clean_prefix}{ctx.command.qualified_name}{C.RESET}: {C.RED}{error.message}```")

        elif isinstance(error, CheckFailure):
            return

        elif isinstance(error, CheckAnyFailure):
            return

        else:
            await self.bot.clear_actions()
            await self.error(ctx, error,
                             f"```ansi\n{C.YELLOW}{ctx.clean_prefix}{ctx.command.qualified_name}{C.RESET}: {C.RED}An unknown error occurred: {C.GOLD}{repr(error)}{C.RESET}```")

    async def error(
            self,
            ctx: Context,
            error: Exception,
            message: str = None
    ) -> None:
        await ctx.message.edit(content=message, delete_after=5)
        if self.bot.cfg["logging"]["error_logging"]:
            print(
                f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Error in command {F.YELLOW}{ctx.command.name}{F.LIGHTBLACK_EX}: {F.RED}{error}")


async def setup(bot: Axio):
    await bot.add_cog(Errors(bot))
