import discord
from meowbot.utils import logging, setup_logger


class HelperService:
    def __init__(self):
        self.logger = setup_logger(name="service.helper", level=logging.INFO)
        self.logo_url = (
            "https://github.com/jaimegarjr/meowBot/blob/main/meowbot/bot/images/logo.jpg?raw=true"
        )

    def serve_help_command_embed(self):
        embed = discord.Embed(
            title="**meowBot >.< General Commands**",
            description="**Some useful commands to access meowBot:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=self.logo_url)
        embed.add_field(
            name="```m.help (none, music, misc)```",
            value="Lists commands pertaining to a particular topic.",
            inline=False,
        )
        embed.add_field(name="```m.intro```", value="Greets the user.", inline=False)
        embed.add_field(name="```m.users```", value="Prints number of users.", inline=False)
        embed.add_field(
            name="```m.purge (num)```",
            value="Purges however many messages you provide it prior to sending command.",
            inline=False,
        )
        embed.add_field(
            name="```m.invite```",
            value="Provides the user with a link to invite meowBot to different servers!",
            inline=False,
        )
        self.logger.info("Help command embed served.")
        return embed

    def serve_music_command_embed(self):
        embed = discord.Embed(
            title="**meowBot >.< Music Commands**",
            description="**Some useful commands to access meowBot's music functionality:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=self.logo_url)
        embed.add_field(
            name="```m.join```",
            value="Adds the bot to a voice channel if user is already in one. "
            "Otherwise, nothing will happen.",
            inline=False,
        )
        embed.add_field(
            name="```m.leave```",
            value="Takes meowBot out of whatever channel the user is in.",
            inline=False,
        )
        embed.add_field(
            name="```m.play (url)```",
            value="Plays a song from youtube given by the user.",
            inline=False,
        )
        embed.add_field(
            name="```m.pause```",
            value="Pauses the current song playing.",
            inline=False,
        )
        embed.add_field(
            name="```m.resume```",
            value="Resumes the current song on queue.",
            inline=False,
        )
        embed.add_field(
            name="```m.stop```",
            value="Completely stops any audio from playing on meowBot.",
            inline=False,
        )
        embed.add_field(
            name="```m.queue```",
            value="Prints the current queue of songs.",
            inline=False,
        )
        embed.add_field(
            name="```m.skip```",
            value="Skips the current song playing.",
            inline=False,
        )
        embed.add_field(
            name="```m.clear```",
            value="Clears the current queue of songs.",
            inline=False,
        )
        self.logger.info("Music subcommand embed served.")
        return embed

    def serve_channels_command_embed(self):
        embed = discord.Embed(
            title="**meowBot >.< Channel Commands**",
            description="**NOTE**: You need the *Manage Channels* "
            "permission to use these commands.\n"
            "**Some useful commands to create and delete channels with meowBot:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=self.logo_url)
        embed.add_field(
            name="```m.create (name)```",
            value="Creates a basic text channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.create voice (name)```",
            value="Creates a basic voice channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.create priv (name)```",
            value="Creates a private text channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.create priv_voice (name)```",
            value="Creates a private voice channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.delete (name)```",
            value="Deletes a voice / text channel with the given name.",
            inline=False,
        )
        self.logger.info("Channels subcommand embed served.")
        return embed

    def serve_misc_command_embed(self):
        embed = discord.Embed(
            title="**meowBot >.< Misc Commands**",
            description="**Some fun and miscellaneous functions that meowBot offers:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=self.logo_url)
        embed.add_field(
            name="```m.quote```",
            value="Prints a random quote for you fellas feeling under the weather.",
            inline=False,
        )
        embed.add_field(
            name="```m.github```",
            value="Gives the caller a link to the github repo that meowBot runs off of.",
            inline=False,
        )
        embed.add_field(
            name="```m.dadjoke```",
            value="Provides the user with a funny dad joke, if you're into that stuff.",
            inline=False,
        )
        embed.add_field(
            name="```m.profile (user tag)```",
            value="Sends the user a detailed tag of their profile on Discord.",
            inline=False,
        )
        self.logger.info("Misc subcommand embed served.")
        return embed
