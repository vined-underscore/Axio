import asyncio
import json
import threading
import typing
import colorama
import time
import datetime
import re
import discord
import nest_asyncio
import os
from util.token import get_token_data
from colorama import Fore as F
from util.colors import Colors as C
from util.embedder import get_embed_link
from discord import Webhook
from discord.ext import commands
from discord.ext.commands import (
    Context,
    Command
)

colorama.init()
config_template = """{
    "prefixes": [
        "ax."
    ],
    "logging": {
        "enabled": true,
        "error_logging": true,
        "events": {
            "member_joined": false,
            "member_left": false,
            "bot_joined_server": true,
            "bot_left_server": true,
            "commands": true
        }
    },
    "nitro_sniper": {
        "enabled": true,
        "webhook": {
            "enabled": true,
            "url": "",
            "ping_everyone": true
        },
        "ignore_self": false
    },
    "help_command": {
        "command_help_videos": false
    },
    "nuke": {
        "server_name": "Nuked by Axio",
        "channel_names": [
            "nuked-by-axio",
            "fucked-by-axio"
        ],
        "webhook_names": [
            "Axio"
        ],
        "webhook_messages": [
            "@everyone Nuked by Axio https://discord.gg/suyg2jVA"
        ]
    }
}"""


class Axio(commands.Bot):
    def __init__(
            self,
            *args,
            initial_extensions: list[str],
            is_main: bool,
            cfg_filepath: str,
            data_path: str,
            tokens: list[str],
            **kwargs,
    ):
        nest_asyncio.apply()
        colorama.init()
        super().__init__(*args, **kwargs)
        self.version = "1.0.1"
        self.author = {
            "name": "vined_",  # I will hang myself if you SKID DON'T DO IT PLEASE
            "id": 1119679354306297918,  # I will hang myself if you SKID DON'T DO IT PLEASE
        }

        self.has_printed_stats = False
        self.cfg_path = cfg_filepath
        self.tokens = tokens
        self.data_path = data_path
        self.cfg = self.update_config()
        self.is_main = is_main
        self.initial_extensions = initial_extensions
        self.start_time = time.time()
        self.em_thumbnail = "https://media.discordapp.net/attachments/1139901136128721009/1212184056452620308/V5OzrAD.png?ex=65f0e960&is=65de7460&hm=eaa8cd1dc4e436caa7a3e181229df8b84686c4201c6240e792a70b13f1535df2&=&format=webp&quality=lossless"
        self.messages_count = 0
        self.is_spamming = False
        self.is_channel_spamming = False
        self.is_role_spamming = False
        self.is_banning = False
        self.is_spamming_gc = False
        self.is_purging = False
        self.is_massmentioning = False
        self.is_nuking = False
        self.nitro_hook = None
        self.spam_message = None
        self.snipe_dict: dict[int, list[discord.Message]] = {}
        self.edit_snipe_dict: dict[int, dict[str, discord.Message]] = {}
        self.copycat_ids = []
        self.animating = {
            "name": "",
            "frame_index": 0,
            "show_info": False,
            "message": {
                "id": 0,
                "channel_id": 0
            },
            "is_animating": False
        }
        asyncio.create_task(self.clear_actions())

    async def clear_actions(self):
        self.is_spamming = False
        self.is_channel_spamming = False
        self.is_role_spamming = False
        self.is_banning = False
        self.is_spamming_gc = False
        self.animating["is_animating"] = False
        self.is_purging = False
        self.is_massmentioning = False
        self.is_nuking = False
        try:
            await self.spam_message.delete()
        except AttributeError:
            pass

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(
                    f"{F.LIGHTBLACK_EX}Error while loading extension {F.YELLOW}{extension}{F.LIGHTBLACK_EX}: {F.RED}{e}{F.LIGHTBLACK_EX}.\n")
                exit()

            if self.is_main:
                print(f"{F.LIGHTBLACK_EX}Loaded extension {F.YELLOW}{extension}{F.LIGHTBLACK_EX}.")

        if self.is_main:
            print(f"{F.LIGHTBLACK_EX}Connecting...{F.RESET}")

        self.start_time: float = time.time()

    async def command_help_link(self, ctx: Context, command: Command) -> str:
        param_str = ""
        boolean_param: commands.Parameter | None = None
        for param in command.params.values():
            param_str += f"[{param.name}] "
            if param.annotation == bool or param.annotation == typing.Optional[bool]:
                boolean_param = param

        embed = discord.Embed(
            title=f"{command.name.capitalize()} Command Usage",
            description=f"""
Description: {command.description or command.short_doc or command.brief}
Aliases: {", ".join([f"{ctx.clean_prefix}{alias}" for alias in command.aliases]) if command.aliases else "None"}
Usage: {ctx.clean_prefix}{command.qualified_name} {param_str}""",
            color=0xB59410
        )
        # This only handles one parameter in the command
        if boolean_param is not None:
            embed.description += f"\n\nThe parameter {boolean_param.name} is a boolean.\nYou can enter 1 (true) or 0 (false)\nYou can also enter true or false."

        provider = f"{self.author['name']} ({self.author['id']})"
        embed.set_author(name=f"Axio v{self.version}", url=None)
        link = await get_embed_link(embed, provider)
        if self.cfg["help_command"]["command_help_videos"]:
            with open("./tutorial/videos.json") as f:
                data = json.load(f)

            if data.get(command.name):
                link = await get_embed_link(embed, provider, data.get(command.name))
            else:
                link = await get_embed_link(embed, provider)

        return link

    def get_uptime(self) -> str:
        uptime = round(time.time() - self.start_time)
        return str(datetime.timedelta(seconds=int(uptime)))

    def update_config(self) -> dict:
        with open(self.cfg_path, "r") as f:
            self.cfg = json.load(f)

        if re.search(
                r'discord(?:app)?\.com/api/webhooks/(?P<id>[0-9]{17,20})/(?P<token>[A-Za-z0-9.\-_]{60,68})',
                self.cfg["nitro_sniper"]["webhook"]["url"]
        ):
            self.nitro_hook = Webhook.from_url(self.cfg["nitro_sniper"]["webhook"]["url"], session=None)
        else:
            self.nitro_hook = None

        self.command_prefix = self.cfg["prefixes"]
        return self.cfg

    def can_log(self, event: str) -> bool:
        if not self.has_printed_stats and self.is_main:
            return False

        if not self.cfg["logging"]["enabled"]:
            return False

        if not self.cfg["logging"]["events"].get(event):
            return False

        return True

    async def banner(self) -> None:
        self.has_printed_stats = False
        print(C.fade_horizontal((255, 215, 0), (20, 20, 20), f"""
⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⢀⣤⣤⣄⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⣶⣿⣷⣆⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⠸⣿⣿⡿⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⡀⣾⣿⣿⣿⣿⡇⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⣰⣿⣿⣿⣿⣿⣿⡄⡀⡀⡀⣾⣿⣶⡄⡀⣰⣿⣿⡆⢠⣶⣿⡆⡀⡀⣀⣶⣿⣿⣿⣿⣷⣦⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⢰⣿⣿⡿⡀⠘⣿⣿⣿⡀⡀⡀⠘⢿⣿⣷⣾⣿⣿⠇⡀⢸⣿⣿⡇⡀⢰⣿⣿⡿⠉⠈⠛⣿⣿⣿⡄⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⢠⣾⣿⣿⣧⣀⣠⣽⣿⣿⣷⡀⡀⡀⠈⣿⣿⣿⣿⡃⡀⡀⢸⣿⣿⡇⡀⣿⣿⣿⠁⡀⡀⡀⢸⣿⣿⡇⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⣾⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⡇⡀⡀⣸⣿⣿⣿⣿⣷⡄⡀⢸⣿⣿⡇⡀⢻⣿⣿⡄⡀⡀⡀⣸⣿⣿⡇⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⣴⣿⣿⡏⡀⡀⡀⡀⡀⠈⢿⣿⣿⣦⣼⣿⣿⠏⠙⢿⣿⣷⣄⢸⣿⣿⡇⡀⠘⣿⣿⣿⣦⣤⣾⣿⣿⡟⠁⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⠛⠛⠛⡀⡀⡀⡀⡀⡀⡀⠘⠛⠛⠛⠛⠟⠃⡀⡀⠈⠛⠻⠋⠈⠛⠻⠃⡀⡀⡀⠙⠻⠿⠿⠿⠛⠋⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀
⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀""", 2))
        print(f"		    {F.YELLOW}v{self.version}")
        await asyncio.sleep(3)
        print(
            f"\n{F.YELLOW}Axio {F.LIGHTBLACK_EX}by {F.LIGHTRED_EX}{self.author['name']} ({self.author['id']}){F.RESET}")
        print(
            f"{F.YELLOW}Axio{F.LIGHTBLACK_EX} is running on {F.YELLOW}{len(self.tokens)}{F.LIGHTBLACK_EX} account(s){F.RESET}\n")

        print(f"{F.LIGHTBLACK_EX}Logged in {F.YELLOW}{self.user.name} ({self.user.id}){F.RESET}")
        print(
            f"{F.LIGHTBLACK_EX}Prefixes: {F.YELLOW}{f'{F.LIGHTBLACK_EX}, {F.YELLOW}'.join(self.cfg['prefixes'])}{F.RESET}")
        print(f"{F.LIGHTBLACK_EX}Commands: {F.YELLOW}{len(self.commands)}{F.LIGHTBLACK_EX}")

        print(
            f"\n{F.LIGHTBLACK_EX}Logging: {f'{F.GREEN}Enabled' if self.cfg['logging']['enabled'] else f'{F.RED}Disabled'}")
        print(
            f"{F.LIGHTBLACK_EX}Error Logging: {f'{F.GREEN}Enabled' if self.cfg['logging']['error_logging'] else f'{F.RED}Disabled'}")
        print(
            f"{F.LIGHTBLACK_EX}Nitro Sniper: {f'{F.GREEN}Enabled' if self.cfg['nitro_sniper']['enabled'] else f'{F.RED}Disabled'}{F.RESET}\n")
        self.has_printed_stats = True

async def start(token: str):
    with open("./configs/tokens.json", "r") as f:
        tokens = json.load(f)

    if tokens["tokens"]["main"] == "" and tokens["tokens"]["other"] == []:
        print(f"{F.LIGHTBLACK_EX}You didn't put any tokens in {F.YELLOW}./configs/tokens.json{F.RESET}")
        exit()

    if tokens["tokens"]["main"] == "":
        print(f"{F.LIGHTBLACK_EX}You didn't put a main token in {F.YELLOW}./configs/tokens.json{F.RESET}")
        exit()

    token_data = await get_token_data(token)
    if not token_data[0]:
        print(f"{F.LIGHTBLACK_EX}Invalid token {F.YELLOW}{token}{F.RESET}")
        exit()

    data = token_data[1]
    cfg_path = f"./configs/{data['id']}"
    data_path = f"./data/{data['id']}"
    if not os.path.isdir(cfg_path):
        os.makedirs(cfg_path)

        with open(cfg_path + "/config.json", "w") as f:
            f.write(config_template)
            print(
                f"{F.RESET}[{F.YELLOW}{data['username']} {data['id']}{F.RESET}] {F.LIGHTBLACK_EX}Succesfully created config file {F.CYAN}{cfg_path}/config.json{F.LIGHTBLACK_EX}. If you want to modify it, you can apply the changes then use the {F.YELLOW}updatecfg{F.LIGHTBLACK_EX} command.")

    if not os.path.isdir(data_path):
        os.makedirs(data_path)

    path = os.path.abspath(data_path)
    files = [
        "/animate/animations.json",
        "/friends/friends.json",
        "/fun/fake_ips.json",
        "/fun/fake_tokens.json"
    ]
    folders = [
        "/servers",
        "/tokens",
        "/users",
        "/groups"
    ]
    for file in files:
        if not os.path.isdir(path + "/" + file.split("/")[1]):
            os.makedirs(path + "/" + file.split("/")[1])
            with open(path + file, "w+") as f:
                f.write("{}")

    for folder in folders:
        if not os.path.isdir(path + folder):
            os.makedirs(path + folder)

    with open(cfg_path + "/config.json", "r") as f:
        cfg = json.load(f)

    exts = [
        "events",
        "raid",
        "utility",
        "errors",
        "fun",
        "dev",
        "help",
        "nitro"
    ]
    with open("./configs/tokens.json", "r") as f:
        data = json.load(f)
        _tokens = [val for sublist in data["tokens"].values() for val in
                   (sublist if isinstance(sublist, list) else [sublist])]

    async with Axio(
            command_prefix=cfg["prefixes"],
            initial_extensions=[f"cmds.{ext}" for ext in exts],
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True,
            is_main=True if token == tokens["tokens"]["main"] else False,
            cfg_filepath=cfg_path + "/config.json",
            data_path=data_path,
            tokens=_tokens,
            self_bot=True,
    ) as bot:
        try:
            await bot.start(token)
        except Exception as e:
            print(f"{F.LIGHTBLACK_EX}Error while starting the bot: {F.RED}{e}{F.LIGHTBLACK_EX}.")
            exit()


def start_threads():
    with open("./configs/tokens.json", "r") as f:
        data = json.load(f)
        tokens = [val for sublist in data["tokens"].values() for val in
                  (sublist if isinstance(sublist, list) else [sublist])]

    threads = []
    for token in tokens:
        thread = threading.Thread(target=asyncio.run, args=(start(token),))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_threads()
