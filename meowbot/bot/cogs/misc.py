import random
import discord
from discord.ext import commands
from meowbot.application import HttpClient
from meowbot.utils import logging, setup_logger


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.misc", level=logging.INFO)
        self.http_client = HttpClient(
            base_url="https://programming-quotes-api.azurewebsites.net/api", timeout=10
        )
        self.quotes_path = "meowbot/bot/files/quotes.txt"
        self.jokes_path = "meowbot/bot/files/jokes.txt"

    @commands.hybrid_command(name="quote", description="Sends a random programming quote")
    async def quote(self, ctx):
        # https://programming-quotes-api.azurewebsites.net/api/quotes/random
        # res = self.http_client.get("/quotes/random")
        quote = random.choice(list(open(self.quotes_path)))
        await ctx.channel.send(quote)
        self.logger.info(f"Random quote was sent to {ctx.author} in {ctx.channel}.")

    @commands.hybrid_command(name="github", description="Sends the GitHub link for meowBot")
    async def github(self, ctx):
        await ctx.channel.send(
            "Here's what I'm built off of. "
            "If you'd like to contribute, fork and create a pull request! Github: "
            "https://github.com/JJgar2725/meowBot"
        )
        self.logger.info(f"Github link was sent to {ctx.author} in {ctx.channel}.")

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


async def setup(bot):
    await bot.add_cog(Misc(bot))
