from app.bot.commands import handle_help, handle_start, handle_status, handle_unknown
from app.bot.dispatcher import Dispatcher
from app.bot.schemas import TelegramChat, TelegramMessage, TelegramUpdate, TelegramUser


def test_help_command_shows_usage() -> None:
    help_text = handle_help()

    assert "Bot usage:" in help_text
    assert "/start - start or refresh your session" in help_text
    assert "/help - show this help message" in help_text
    assert "/status - check bot status" in help_text


def test_dispatcher_routes_start_command() -> None:
    update = TelegramUpdate(
        update_id=1,
        message=TelegramMessage(
            message_id=10,
            chat=TelegramChat(id=100, type="private"),
            text="/start",
            from_user=TelegramUser(id=200, username="alice"),
        ),
    )

    assert Dispatcher().dispatch(update) == handle_start()


def test_other_commands_still_return_text() -> None:
    assert handle_status()
    assert handle_unknown()
