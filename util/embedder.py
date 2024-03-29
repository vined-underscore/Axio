import discord
import aiohttp
from urllib.parse import quote


async def get_embed_link(
    embed: discord.Embed,
    provider: str = None,
    video_url: str = None
) -> str | None:
    if embed.fields:
        return None

    description = quote(embed.description) if embed.description else ""
    title = quote(embed.title) if embed.title else ""
    provider = quote(provider) if provider else ""
    author = quote(embed.author.name) if embed.author.name else ""
    thumbnail = quote(embed.thumbnail.url) if embed.thumbnail else ""
    color = quote(Embedder.rgb_to_hex(embed.colour.to_rgb())) if embed.color else ""
    media_type = "none" if not thumbnail else "thumbnail"
    if video_url:
        thumbnail = quote(video_url)
        media_type = "video"

    url = f"https://embedl.ink/?deg=&provider={provider}&providerurl=&author={author}&authorurl=&title={title}&color={color}&media={media_type}&mediaurl={thumbnail}&desc={description}"
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://embedl.ink/api/create",
                data={
                    "url": url.replace("https://embedl.ink/", ""),
                    "providerName": provider,
                    "providerUrl": "",
                    "authorName": author,
                    "authorUrl": "",
                    "title": title,
                    "mediaType": media_type,
                    "mediaUrl": thumbnail,
                    "mediaThumb": None,
                    "description": description
                }
        ) as r:
            data = await r.json()
            if data.get("success"):
                code = data["code"]

        return f"https://embedl.ink/e/{code}"

def rgb_to_hex(
    rgb: tuple
) -> str:
    if len(rgb) != 3:
        return "#FFFFFF"

    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
