import os
import discord
from discord.ext import commands
from meowbot.application import HttpClient
from meowbot.utils import logging, setup_logger
from urllib.parse import urlencode


class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.interaction", level=logging.INFO)
        self.logo_url = "https://github.com/jaimegarjr/meowBot/blob/main/meowbot/bot/images/logo.jpg?raw=true"
        self.prog_quote_client = HttpClient(
            base_url="https://programming-quotes-api.azurewebsites.net/api", timeout=10
        )
        self.dad_joke_client = HttpClient(
            base_url="https://icanhazdadjoke.com",
            headers={"Accept": "application/json"},
            timeout=10,
        )

    @commands.hybrid_command(name="intro", description="Greets the user")
    async def intro(self, ctx):
        await ctx.channel.send("Well, hai! :3 I'm jaimegarjr's cat-based discord bot!")
        self.logger.info("User requested intro message.")

    @commands.hybrid_command(name="github", description="Sends the GitHub link for meowBot")
    async def github(self, ctx):
        await ctx.channel.send(
            "Here's what I'm built off of. "
            "If you'd like to contribute, fork and create a pull request! Github: "
            "https://github.com/JJgar2725/meowBot"
        )
        self.logger.info(f"Github link was sent to {ctx.author} in {ctx.channel}.")

    @commands.hybrid_command(
        name="invite", description="Provides the user with a link to invite meowBot"
    )
    async def invite(self, ctx):
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
            kick_members=True
        )

        params = {
            "client_id": client_id,
            "permissions": permissions.value,
            "scope": "bot applications.commands"
        }

        invite_link = f"https://discord.com/oauth2/authorize?{urlencode(params)}"

        embed = discord.Embed(
            title="Invite meowBot :3",
            description=f"Click [here]({invite_link}) to invite me to another server!",
            color=discord.Color.light_gray()
        )
        embed.set_thumbnail(url=self.logo_url)

        await ctx.send(embed=embed)
        self.logger.info(f"User {ctx.author} requested invite link.")

    @commands.hybrid_command(name="profile", description="Sends a detailed profile of a user")
    async def profile(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
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
        await ctx.send(embed=embed)
        self.logger.info(f"User {user} requested their profile.")

    @commands.hybrid_command(name="users", description="Prints number of users")
    async def users(self, ctx):
        guild_members = ctx.guild.member_count
        users_embed = discord.Embed(
            title="**Current User Count on Guild!**",
            description=f"""Number of Members: {guild_members}""",
            colour=discord.Colour.green(),
        )
        await ctx.channel.send(content=None, embed=users_embed)
        self.logger.info(f"User requested user count of guild {ctx.guild}.")

    @commands.hybrid_command(
        name="purge", description="Purges however many messages you provide it"
    )
    async def purge(self, ctx, arg):
        await ctx.channel.purge(limit=(int(arg) + 1))
        self.logger.info(f"User {ctx.author} purged {arg} messages in {ctx.channel}.")

    @commands.hybrid_command(name="quote", description="Sends a random programming quote")
    async def quote(self, ctx):
        res = await self.prog_quote_client.get("/quotes/random")
        quote = res.get("text") + " - " + res.get("author")
        await ctx.channel.send(quote)
        self.logger.info(f"Random quote was sent to {ctx.author} in {ctx.channel}.")

    @commands.hybrid_command(name="dadprogjoke", description="Sends a random dad joke")
    async def dadprogjoke(self, ctx):
        res = await self.dad_joke_client.get("/")
        quote = res.get("joke")

        embed = discord.Embed(
            title="**Random Dad Joke**",
            description="**Fetched from icanhazdadjoke.com!**",
            color=discord.Colour.light_grey(),
        )
        embed.add_field(name="```Joke```", value=f"{quote}", inline=False)
        await ctx.channel.send(content=None, embed=embed)
        self.logger.info(f"Dad-styled programming joke was sent to {ctx.author} in {ctx.channel}.")


async def setup(bot):
    await bot.add_cog(Interactions(bot))
