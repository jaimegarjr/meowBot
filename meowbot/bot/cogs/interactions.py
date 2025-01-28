import discord
from discord.ext import commands
from meowbot.utils import logging, setup_logger
from meowbot.application.services.interactions_service import InteractionsService


class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interactions_service = InteractionsService()
        self.logger = setup_logger(name="cog.interactions", level=logging.INFO)

    @commands.hybrid_command(name="intro", description="Greets the user")
    async def intro(self, ctx):
        message = self.interactions_service.serve_intro_command()
        await ctx.channel.send(message)
        self.logger.info("User requested intro message.")

    @commands.hybrid_command(name="github", description="Sends the GitHub link for meowBot")
    async def github(self, ctx):
        embed = self.interactions_service.serve_github_command()
        await ctx.send(embed=embed)
        self.logger.info(f"Github link was sent to {ctx.author} in {ctx.channel}.")

    @commands.hybrid_command(
        name="invite", description="Provides the user with a link to invite meowBot"
    )
    async def invite(self, ctx):
        embed = self.interactions_service.serve_invite_command()
        await ctx.send(embed=embed)
        self.logger.info(f"User {ctx.author} requested invite link.")

    @commands.hybrid_command(name="profile", description="Sends a detailed profile of a user")
    async def profile(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        embed = self.interactions_service.serve_profile_command(user)
        await ctx.send(embed=embed)
        self.logger.info(f"User {user} requested their profile.")

    @commands.hybrid_command(name="users", description="Prints number of users")
    async def users(self, ctx):
        embed = self.interactions_service.serve_users_command(ctx.guild)
        await ctx.channel.send(content=None, embed=embed)
        self.logger.info(f"User requested user count of guild {ctx.guild}.")

    @commands.hybrid_command(
        name="purge", description="Purges however many messages you provide it"
    )
    async def purge(self, ctx, arg):
        await ctx.channel.purge(limit=(int(arg) + 1))
        self.logger.info(f"User {ctx.author} purged {arg} messages in {ctx.channel}.")

    @commands.hybrid_command(name="quote", description="Sends a random programming quote")
    async def quote(self, ctx):
        quote = await self.interactions_service.serve_quote_command()
        await ctx.channel.send(quote)
        self.logger.info(f"Random quote was sent to {ctx.author} in {ctx.channel}.")

    @commands.hybrid_command(name="dadjoke", description="Sends a random dad joke")
    async def dadjoke(self, ctx):
        embed = await self.interactions_service.serve_dad_joke_command()
        await ctx.channel.send(content=None, embed=embed)
        self.logger.info(f"Dad-styled joke was sent to {ctx.author} in {ctx.channel}.")


async def setup(bot):
    await bot.add_cog(Interactions(bot))
