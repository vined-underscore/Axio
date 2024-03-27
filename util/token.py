from typing import Any
from aiohttp import ClientSession


class Token:
    @staticmethod
    async def check_token(token: str) -> tuple[bool, dict | None]:
        async with ClientSession() as client:
            async with client.get(
                    "https://discord.com/api/v9/users/@me",
                    headers={"Authorization": token}
            ) as r:
                if r.status == 200 or r.status == 204:
                    return True, await r.json()

                return False, None
