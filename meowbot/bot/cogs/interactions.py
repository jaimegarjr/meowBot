import os
import json
import random
import discord
from discord.ext import commands
from meowbot.application import HttpClient
from meowbot.utils import logging, setup_logger


class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.interaction", level=logging.INFO)
        self.http_client = HttpClient(
            base_url="https://programming-quotes-api.azurewebsites.net/api", timeout=10
        )
        self.quotes_path = "meowbot/bot/files/quotes.txt"
        self.jokes_path = "meowbot/bot/files/jokes.txt"

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
        permissions = discord.Permissions.none()
        permissions.manage_roles = True
        permissions.manage_channels = True
        permissions.view_channel = True
        permissions.send_messages = True
        permissions.manage_messages = True
        permissions.embed_links = True
        permissions.attach_files = True
        permissions.read_message_history = True
        permissions.use_external_emojis = True
        permissions.add_reactions = True
        permissions.connect = True
        permissions.speak = True
        permissions.ban_members = True
        permissions.kick_members = True
        link = discord.utils.oauth_url(client_id, permissions=permissions, redirect_uri=None)
        await ctx.send(f"<{link}>")
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
        # https://programming-quotes-api.azurewebsites.net/api/quotes/random
        # res = self.http_client.get("/quotes/random")
        quote = random.choice(list(open(self.quotes_path)))
        await ctx.channel.send(quote)
        self.logger.info(f"Random quote was sent to {ctx.author} in {ctx.channel}.")

    @commands.hybrid_command(name="dadprogjoke", description="Sends a dad-styled programming joke")
    async def dadprogjoke(self, ctx):
        quote = random.choice(list(open(self.jokes_path)))
        quoteQ = quote[1 : quote.find("A")]
        quoteA = quote[quote.find("A") - 1 : -2]

        embed = discord.Embed(
            title="**Dad-Styled Programming Joke**",
            description="**Chosen at random!**",
            color=discord.Colour.light_grey(),
        )
        embed.add_field(name="```Question```", value=quoteQ, inline=False)
        embed.add_field(name="```Answer```", value=quoteA, inline=False)
        await ctx.channel.send(content=None, embed=embed)
        self.logger.info(f"Dad-styled programming joke was sent to {ctx.author} in {ctx.channel}.")


async def setup(bot):
    await bot.add_cog(Interactions(bot))
