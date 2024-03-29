import discord
from util.colors import Colors as C
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands._types import Check

def guild_only() -> Check:
    async def predicate(ctx: Context) -> bool:
        if not isinstance(ctx.channel, discord.abc.GuildChannel):
            await ctx.message.edit(
                content=f"```ansi\n{C.RED}You can only run this command in servers.```",
                delete_after=5
            )
            return False

        return True

    return commands.check(predicate)

def group_only() -> Check:
    async def predicate(ctx: Context) -> bool:
        if not isinstance(ctx.channel, discord.GroupChannel):
            await ctx.message.edit(
                content=f"```ansi\n{C.RED}You can only run this command in group chats.```",
                delete_after=5
            )
            return False

        return True

    return commands.check(predicate)
