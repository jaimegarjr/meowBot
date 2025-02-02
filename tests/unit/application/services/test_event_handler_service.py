import pytest
from unittest.mock import Mock, AsyncMock
from meowbot.application.services.event_handler_service import EventHandlerService


def test_event_handler_service_initialization():
    """Test the initialization of EventHandlerService."""
    event_handler = EventHandlerService()

    assert event_handler is not None
    assert event_handler.logger is not None
    assert event_handler.logger.name == "service.event.handler"
    assert event_handler.logger.level == 20


@pytest.mark.asyncio
async def test_serve_on_guild_join_embed():
    """Test the serve_on_guild_join_embed method."""
    event_handler = EventHandlerService()
    guild = Mock()

    text_channel = Mock()
    text_channel.send = AsyncMock()
    text_channel.permissions_for.return_value.send_messages = True
    guild.text_channels = [text_channel]

    await event_handler.serve_on_guild_join_event(guild)
    assert guild.text_channels[0].send.called is True
