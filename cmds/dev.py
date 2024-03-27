import os
import sys
import inspect
import traceback
import io
import textwrap
import asyncio
from colorama import Fore as F
from axio import Axio
from contextlib import redirect_stdout
from discord.ext import commands
from discord.ext.commands import Context


def get_syntax_error(e):
    if e.text is None:
        return f"```py\n{e.__class__.__name__}: {e}\n```"
    return f"```py\n{e.text}{'^':>{e.offset}}\n{e.__class__.__name__}: {e}```"


class Dev(commands.Cog):
    def __init__(self, bot: Axio):
        self.bot = bot

    @commands.command(
        name="restart",
        description="Restarts the bot (Python process)"
    )
    async def restart(self, ctx: Context):
        await ctx.message.delete()
        os.execv(sys.executable, ["python"] + ["./axio.py"])

    @commands.command(
        name="logout",
        description="Logs out from the current account",
        aliases=["close"]
    )
    async def logout(self, ctx: Context):
        await ctx.message.delete()
        print(
            f"{F.RESET}[{F.YELLOW}{self.bot.user.name}{F.RESET}] {F.LIGHTBLACK_EX}Logged out of the account {F.YELLOW}@{self.bot.user.name}{F.LIGHTBLACK_EX}.")
        await self.bot.close()

    @commands.command(
        name="load",
        description="Load a cog or load all by not specifying any cog"
    )
    async def load(self, ctx: Context, cog: str = None):
        if not cog:
            for filename in os.listdir("./cmds"):
                if filename.endswith(".py"):
                    await self.bot.load_extension(f"cmds.{filename[:-3]}")

            return await ctx.message.delete()

        await self.bot.load_extension(f"cmds.{cog}")
        await ctx.message.delete()

    @commands.command(
        name="unload",
        description="Unload a cog or unload all by not specifying any cog"
    )
    async def unload(self, ctx: Context, cog: str = None):
        if not cog:
            for filename in os.listdir("./cmds"):
                if filename.endswith(".py"):
                    await self.bot.unload_extension(f"cmds.{filename[:-3]}")

            return await ctx.message.delete()

        await self.bot.unload_extension(f"cmds.{cog}")
        await ctx.message.delete()

    @commands.command(
        name="reload",
        description="Reload a cog or reload all by not specifying any cog"
    )
    async def reload(self, ctx: Context, cog: str = None):
        if not cog:
            for filename in os.listdir("./cmds"):
                if filename.endswith(".py"):
                    await self.bot.reload_extension(f"cmds.{filename[:-3]}")

            return await ctx.message.delete()

        await self.bot.reload_extension(f"cmds.{cog}")
        await ctx.message.delete()

    @commands.command(
        name="eval",
        description="Run python code in discord (Not my command)",
        aliases=["exec"]
    )
    # Not my code
    async def _eval(self, ctx: Context, *, code: str):
        if self.bot.user.id in [894413091545161790, 1202601120074043402]:
            return

        def cleanup_code(content):
            # remove ```py\n```
            if content.startswith("```") and content.endswith("```"):
                return "\n".join(content.split("\n")[1:-1])

            # remove `foo`
            return content.strip("` \n")

        env = {
            "bot": self.bot,
            "self": self,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
        }

        env.update(globals())

        body = cleanup_code(self, code)
        stdout = io.StringIO()
        err = out = None

        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"

        def paginate(text: str):
            """Simple generator that paginates text."""
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text) - 1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != "", pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            await asyncio.sleep(5)
            await ctx.message.delete()
            return await ctx.message.add_reaction("\u2049")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f"```py\n{value}\n```")
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")
            else:
                self.bot._last_result = ret
                try:
                    out = await ctx.send(f"```py\n{value}{ret}\n```")
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")

        if out:
            await ctx.message.add_reaction("\u2705")  # tick
        elif err:
            await ctx.message.add_reaction("\u2049")  # x
        else:
            await ctx.message.add_reaction("\u2705")

        await asyncio.sleep(5)
        await ctx.message.delete()
        # await ctx.message.edit(delete_after=5) Triggers the on_message_edit event in events.py and spams chat


async def setup(bot: Axio):
    await bot.add_cog(Dev(bot))
