import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from meowbot.bot.meowbot import MeowBot


@pytest.fixture
def bot_instance():
    """Fixture to create a MeowBot instance."""
    with patch("os.environ", {"BOT_TOKEN": "fake_token"}):
        bot = MeowBot()
    return bot


@pytest.mark.asyncio
async def test_meowbot_initialization(bot_instance):
    """Test the initialization of MeowBot."""
    assert bot_instance.bot is not None
    assert bot_instance.bot.command_prefix.__name__ == "get_prefix"
    assert bot_instance.bot.description.startswith("Hi! I'm meowBot.")

    intents = bot_instance.bot.intents
    assert intents.message_content is True
    assert intents.guilds is True


@pytest.mark.asyncio
async def test_meowbot_cogs_loading(bot_instance):
    """Test that MeowBot loads cogs correctly."""
    bot_instance.bot.load_extension = AsyncMock()

    with patch("os.listdir", return_value=["cog1.py", "cog2.py", "__init__.py"]):
        await bot_instance.load_extensions()

    bot_instance.bot.load_extension.assert_any_call("meowbot.bot.cogs.cog1")
    bot_instance.bot.load_extension.assert_any_call("meowbot.bot.cogs.cog2")
    assert bot_instance.bot.load_extension.call_count == 2


# @pytest.mark.asyncio
# async def test_meowbot_run(bot_instance):
#     """Test the bot's run method."""
#     bot_instance.bot.load_extensions = AsyncMock()
#     bot_instance.bot.run = MagicMock()

#     bot_instance.bot.run()
#     bot_instance.bot.run.assert_called_once_with("fake_token")


# @pytest.mark.asyncio
# async def test_meowbot_error_handling(bot_instance):
#     """Test MeowBot handles cog loading errors gracefully."""
#     bot_instance.bot.load_extension = AsyncMock(side_effect=Exception("Error loading cog"))

#     with patch("os.listdir", return_value=["cog1.py"]):
#         await bot_instance.load_extensions()

#     # Ensure error is logged
#     # Assuming you log errors, check the logging output (you may need to mock your logger)
#     bot_instance.logger.error.assert_called_with("Error loading cog meowbot.bot.cogs.cog1: Error loading cog")
