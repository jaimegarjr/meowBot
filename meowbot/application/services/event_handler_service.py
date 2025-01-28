import discord
from meowbot.utils import logging, setup_logger


class EventHandlerService:
    def __init__(self):
        self.logger = setup_logger(name="service.event.handler", level=logging.INFO)
        self.logo_url = (
            "https://github.com/jaimegarjr/meowBot/blob/main/meowbot/bot/images/logo.jpg?raw=true"
        )

    async def serve_on_guild_join_event(self, guild):
        embed = discord.Embed(
            title="Welcome to meowBot!",
            description="I'm meowBot, a Discord bot created by jaimegarjr.",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=self.logo_url)
        embed.add_field(
            name="```m.help```",
            value="Lists all available commands.",
            inline=False,
        )
        embed.add_field(
            name="```Feedback```",
            value="If you have any feedback, drop some on "
            "[this](https://forms.gle/Lxti92YXSKykzfyHA) form!",
            inline=False,
        )
        embed.add_field(
            name="```GitHub```",
            value="Check out the bot's [source code](https://github.com/JJgar2725/meowBot)!",
            inline=False,
        )

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

        self.logger.info(f"Served welcome message to {guild.name}.")
