import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from meowbot.bot.meowbot import MeowBot


@pytest.fixture
def mock_env():
    """Fixture to mock environment variables."""
    with patch("os.environ", {"BOT_TOKEN": "fake_token"}):
        yield


@pytest.fixture
def bot_instance(mock_env):
    """Fixture to create a MeowBot instance."""
    return MeowBot()


@pytest.fixture
def mock_cogs():
    """Fixture to mock cog files."""
    with patch("os.listdir", return_value=["cog1.py", "cog2.py", "__init__.py"]):
        yield


@pytest.mark.asyncio
async def test_meowbot_initialization(bot_instance):
    """Test the initialization of MeowBot."""
    assert bot_instance.bot is not None
    assert bot_instance.bot.command_prefix == "m."
    assert bot_instance.bot.description.startswith("Hi! I'm meowBot.")

    intents = bot_instance.bot.intents
    assert intents.message_content is True
    assert intents.guilds is True


@pytest.mark.asyncio
async def test_meowbot_cogs_loading(bot_instance, mock_cogs):
    """Test that MeowBot loads cogs correctly."""
    bot_instance.bot.load_extension = AsyncMock()
    await bot_instance.load_extensions()

    bot_instance.bot.load_extension.assert_any_call("meowbot.bot.cogs.cog1")
    bot_instance.bot.load_extension.assert_any_call("meowbot.bot.cogs.cog2")
    assert bot_instance.bot.load_extension.call_count == 2


@pytest.mark.asyncio
async def test_meowbot_run(bot_instance, mock_env):
    """Test the bot's run method."""
    bot_instance.bot.run = MagicMock()
    bot_instance.setup = AsyncMock()

    bot_instance.run()

    assert bot_instance.bot.setup_hook == bot_instance.setup
    bot_instance.bot.run.assert_called_once_with("fake_token")


@pytest.mark.asyncio
async def test_meowbot_error_handling(bot_instance, mock_cogs):
    """Test MeowBot handles cog loading errors gracefully."""
    bot_instance.logger = MagicMock()
    bot_instance.bot.load_extension = AsyncMock(side_effect=Exception("Error loading cog"))

    await bot_instance.load_extensions()

    bot_instance.logger.error.assert_called_with("Failed to load extension cog2: Error loading cog")
