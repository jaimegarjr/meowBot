import pytest
from unittest.mock import MagicMock, patch
from meowbot.application.services.voice_service import VoiceService


@pytest.fixture
def mock_bot():
    """Fixture to mock the MeowBot instance"""
    return MagicMock()


@pytest.fixture
def patched_voice_service(mock_bot):
    """Fixture to patch check_leave before instantiation of VoiceService."""
    with patch.object(VoiceService, "check_leave", new_callable=MagicMock) as mock_check_leave:
        service = VoiceService(mock_bot)
        mock_check_leave.start.assert_called_once()
        yield service, mock_check_leave


@pytest.mark.asyncio
async def test_voice_service_initialization(patched_voice_service, mock_bot):
    service, mock_check_leave = patched_voice_service
    mock_check_leave.start.assert_called_once

    assert service.bot == mock_bot
    assert service.music_queue is not None
    assert service.logger is not None
    assert service.logger.name == "service.voice"
