from aiohttp import ClientSession


async def get_token_data(token: str) -> tuple[bool, dict | None]:
    """
    Returns information about a token with the Discord API.

    Attributes
    ----------
    token: str
        The user token.

    Returns
    --------
    tuple[`bool`, `dict` | `None`]
        A tuple containing if the token is invalid or valid (index 0) (False or True) and the user information as a dict (index 1) or None.
    """
    async with ClientSession() as client:
        async with client.get(
                "https://discord.com/api/v9/users/@me",
                headers={"Authorization": token}
        ) as r:
            if r.status == 200 or r.status == 204:
                return True, await r.json()

            return False, None
