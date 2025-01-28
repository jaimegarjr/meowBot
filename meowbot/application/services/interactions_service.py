import os
import discord
from meowbot.application import HttpClient
from meowbot.utils import logging, setup_logger
from urllib.parse import urlencode


class InteractionsService:
    def __init__(self):
        self.logger = setup_logger(name="service.interactions", level=logging.INFO)
        self.logo_url = (
            "https://github.com/jaimegarjr/meowBot/blob/main/meowbot/bot/images/logo.jpg?raw=true"
        )
        self.prog_quote_client = HttpClient(
            base_url="https://programming-quotes-api.azurewebsites.net/api", timeout=10
        )
        self.dad_joke_client = HttpClient(
            base_url="https://icanhazdadjoke.com",
            headers={"Accept": "application/json"},
            timeout=10,
        )

    def serve_intro_command(self):
        self.logger.info("Intro command was served.")
        return "Well, hai! :3 I'm jaimegarjr's cat-based discord bot!"

    def serve_github_command(self):
        self.logger.info("Github command was served.")
        github_link = "https://github.com/JJgar2725/meowBot"
        embed = discord.Embed(
            title="**GitHub Repository**",
            description=f"meowBot is [open-source]({github_link})!",
            color=discord.Colour.light_grey(),
        )
        embed.add_field(name="```Contributions```", value="Feel free to contribute!", inline=False)
        embed.set_thumbnail(url=self.logo_url)
        return embed

    def serve_invite_command(self):
        client_id = os.environ.get("CLIENT_ID")
        if not client_id:
            self.logger.error("CLIENT_ID environment variable is missing.")
            return

        permissions = discord.Permissions(
            manage_roles=True,
            manage_channels=True,
            view_channel=True,
            send_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            use_external_emojis=True,
            add_reactions=True,
            connect=True,
            speak=True,
            ban_members=True,
            kick_members=True,
        )

        params = {
            "client_id": client_id,
            "permissions": permissions.value,
            "scope": "bot applications.commands",
        }

        invite_link = f"https://discord.com/oauth2/authorize?{urlencode(params)}"

        embed = discord.Embed(
            title="Invite meowBot :3",
            description=f"Click [here]({invite_link}) to invite me to another server!",
            color=discord.Color.light_gray(),
        )
        embed.set_thumbnail(url=self.logo_url)
        self.logger.info("Invite link embed served.")
        return embed

    def serve_profile_command(self, user):
        date = str(user.created_at)[:10]
        avatar = user.avatar.replace(static_format="png")
        embed = discord.Embed(
            title="**User Profile**",
            description=f"**Detailed profile for {user}!**",
            color=discord.Colour.light_grey(),
        )
        embed.add_field(name="Username ", value=f"{user.name}", inline=True)
        embed.add_field(name="User ID ", value=f"{user.id}", inline=True)
        embed.add_field(name="Nickname ", value=f"{user.display_name}", inline=True)
        embed.add_field(name="Date Joined ", value=f"{date}", inline=True)
        embed.add_field(name="Mention With ", value=f"{user.mention}", inline=True)
        embed.set_thumbnail(url=avatar)
        self.logger.info(f"Profile embed served for {user}.")
        return embed

    def serve_users_command(self, guild):
        guild_members = guild.member_count
        embed = discord.Embed(
            title="**Current User Count on Guild!**",
            description=f"""Number of Members: {guild_members}""",
            colour=discord.Colour.green(),
        )
        self.logger.info("User count embed served.")
        return embed

    async def serve_quote_command(self):
        res = await self.prog_quote_client.get("/quotes/random")
        quote = res.get("text") + " - " + res.get("author")
        self.logger.info("Random quote was fetched.")
        return quote

    async def serve_dad_joke_command(self):
        res = await self.dad_joke_client.get("/")
        joke = res.get("joke")
        embed = discord.Embed(
            title="**Random Dad Joke**",
            description="**Fetched from icanhazdadjoke.com!**",
            color=discord.Colour.light_grey(),
        )
        embed.add_field(name="```Joke```", value=f"{joke}", inline=False)
        self.logger.info("Dad joke fetched.")
        return embed
