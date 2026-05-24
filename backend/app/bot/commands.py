from __future__ import annotations


def handle_start() -> str:
    return (
        "Welcome to the Telegram Bot Platform. Use /help to see available "
        "commands and /status to check the bot state."
    )


def handle_help() -> str:
    return (
        "Bot usage:\n"
        "• /start - start or refresh your session\n"
        "• /help - show this help message\n"
        "• /status - check bot status\n\n"
        "You can also use the Mini App from the bot menu for the full interface."
    )


def handle_status() -> str:
    return "Bot is running."


def handle_unknown() -> str:
    return "Unknown command. Use /help for available commands."
