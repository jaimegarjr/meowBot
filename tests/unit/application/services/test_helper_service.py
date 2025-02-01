import pytest
import asyncio
import discord
from aioresponses import aioresponses
from meowbot.application.services.helper_service import HelperService

def test_helper_service_initialization():
    """Test the initialization of HelperService."""
    helper = HelperService()

    assert helper is not None
    assert helper.logger is not None
    assert helper.logger.name == "service.helper"
    assert helper.logger.level == 20

def test_serve_help_command_embed():
    """Test the serve_help_command_embed method."""
    helper = HelperService()
    embed = helper.serve_help_command_embed()

    assert embed is not None
    assert embed.title == "**meowBot >.< General Commands**"
    assert embed.description == "**Some useful commands to access meowBot:**"
    assert embed.color == discord.Colour.red()
    assert embed.thumbnail.url == helper.logo_url
    assert len(embed.fields) == 5

def test_serve_music_command_embed():
    """Test the serve_music_command_embed method."""
    helper = HelperService()
    embed = helper.serve_music_command_embed()

    assert embed is not None
    assert embed.title == "**meowBot >.< Music Commands**"
    assert embed.description == "**Some useful commands to access meowBot's music functionality:**"
    assert embed.color == discord.Colour.red()
    assert embed.thumbnail.url == helper.logo_url
    assert len(embed.fields) == 6

def test_serve_misc_command_embed():
    """Test the serve_misc_command_embed method."""
    helper = HelperService()
    embed = helper.serve_misc_command_embed()

    assert embed is not None
    assert embed.title == "**meowBot >.< Misc Commands**"
    assert embed.description == "**Some fun and miscellaneous functions that meowBot offers:**"
    assert embed.color == discord.Colour.red()
    assert embed.thumbnail.url == helper.logo_url
    assert len(embed.fields) == 4

def test_serve_channels_command_embed():
    """Test the serve_channels_command_embed method."""
    helper = HelperService()
    embed = helper.serve_channels_command_embed()

    assert embed is not None
    assert embed.title == "**meowBot >.< Channel Commands**"
    assert embed.description == "**NOTE**: You need the *Manage Channels* " \
            "permission to use these commands.\n" \
            "**Some useful commands to create and delete channels with meowBot:**"
    assert embed.color == discord.Colour.red()
    assert embed.thumbnail.url == helper.logo_url
    assert len(embed.fields) == 5