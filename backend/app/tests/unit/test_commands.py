from app.bot.commands import handle_help, handle_start, handle_status, handle_unknown


def test_help_command_shows_usage() -> None:
    help_text = handle_help()

    assert "Bot usage:" in help_text
    assert "/start - start or refresh your session" in help_text
    assert "/help - show this help message" in help_text
    assert "/status - check bot status" in help_text


def test_other_commands_still_return_text() -> None:
    assert handle_start()
    assert handle_status()
    assert handle_unknown()
