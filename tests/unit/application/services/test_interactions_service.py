import discord
import pytest
from unittest.mock import patch, Mock, AsyncMock
import meowbot.application.services.interactions_service as interactions_service


@pytest.fixture
def mock_env():
    """Fixture to mock environment variables."""
    with patch("os.environ", {"CLIENT_ID": "fake_id"}):
        yield


def test_interactions_service_initialization():
    """Test the initialization of InteractionsService."""
    interactions = interactions_service.InteractionsService()

    assert interactions is not None
    assert interactions.logger is not None
    assert interactions.logger.name == "service.interactions"
    assert interactions.logger.level == 20


def test_serve_intro_command():
    """Test the serve_intro_command method."""
    interactions = interactions_service.InteractionsService()
    message = interactions.serve_intro_command()

    assert message is not None
    assert message == "Well, hai! :3 I'm jaimegarjr's cat-based discord bot!"


def test_serve_github_command():
    """Test the serve_github_command method."""
    interactions = interactions_service.InteractionsService()
    embed = interactions.serve_github_command()
    github_link = "https://github.com/JJgar2725/meowBot"

    assert embed is not None
    assert embed.title == "**GitHub Repository**"
    assert embed.description == f"meowBot is [open-source]({github_link})!"
    assert embed.color == discord.Colour.light_grey()
    assert len(embed.fields) == 1
    assert embed.thumbnail.url == interactions.logo_url


def test_serve_invite_command(mock_env):
    """Test the serve_invite_command method."""
    interactions = interactions_service.InteractionsService()
    embed = interactions.serve_invite_command()
    link = "https://discord.com/oauth2/authorize?client_id=fake_id&" \
        "permissions=271969366&scope=bot+applications.commands"

    assert embed is not None
    assert embed.title == "Invite meowBot :3"
    assert (
        embed.description == f"Click [here]({link}) to invite me to another server!"
    )
    assert embed.color == discord.Colour.light_gray()
    assert embed.thumbnail.url == interactions.logo_url
    assert len(embed.fields) == 0


def test_serve_invite_command_missing_env_var():
    """Test serve_invite_command when CLIENT_ID is missing."""
    interactions = interactions_service.InteractionsService()
    interactions.logger = Mock()

    with patch("os.environ", {}):
        result = interactions.serve_invite_command()

    assert result is None
    interactions.logger.error.assert_called_once_with("CLIENT_ID environment variable is missing.")


def test_serve_profile_command():
    """Test the serve_profile_command method."""
    interactions = interactions_service.InteractionsService()
    user = Mock()
    user.name = "test_user"
    user.id = 1234567890

    embed = interactions.serve_profile_command(user)

    assert embed is not None
    assert embed.title == "**User Profile**"
    assert embed.description == f"**Detailed profile for {user}!**"
    assert embed.color == discord.Colour.light_grey()
    assert len(embed.fields) == 5
    assert embed.fields[0].name == "Username "
    assert embed.fields[0].value == "test_user"
    assert embed.fields[0].inline is True


def test_serve_users_command():
    """Test the serve_users_command method."""
    interactions = interactions_service.InteractionsService()
    guild = Mock()
    guild.member_count = 10

    embed = interactions.serve_users_command(guild)

    assert embed is not None
    assert embed.title == "**Current User Count on Guild!**"
    assert embed.description == "Number of Members: 10"
    assert embed.color == discord.Colour.green()
    assert len(embed.fields) == 0


@pytest.mark.asyncio
async def test_serve_quote_command():
    """Test the serve_quote_command method."""
    interactions = interactions_service.InteractionsService()

    mock_response = {"text": "Code is like humor.", "author": "Unknown"}
    interactions.prog_quote_client.get = AsyncMock(return_value=mock_response)

    quote = await interactions.serve_quote_command()

    expected_quote = "Code is like humor. - Unknown"
    assert quote == expected_quote


@pytest.mark.asyncio
async def test_serve_dad_joke_command():
    """Test the serve_dad_joke_command method."""
    interactions = interactions_service.InteractionsService()

    mock_response = {"joke": "Why do programmers prefer dark mode?"}
    interactions.dad_joke_client.get = AsyncMock(return_value=mock_response)

    embed = await interactions.serve_dad_joke_command()

    assert embed is not None
    assert embed.title == "**Random Dad Joke**"
    assert embed.description == "**Fetched from icanhazdadjoke.com!**"
    assert embed.color == discord.Colour.light_grey()
    assert embed.fields[0].name == "```Joke```"
    assert embed.fields[0].value == "Why do programmers prefer dark mode?"
