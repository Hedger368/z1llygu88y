import asyncio
import contextlib
import io
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import bot


class BotStartupTests(unittest.TestCase):
    def test_import_does_not_start_discord_client(self):
        self.assertFalse(bot.bot.is_ready())

    def test_missing_token_exits_with_helpful_error(self):
        env = dict(os.environ, DISCORD_TOKEN="", PYTHON_DOTENV_DISABLED="1")
        result = subprocess.run(
            [sys.executable, str(Path(bot.__file__))],
            env=env, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Set DISCORD_TOKEN", result.stderr)

    def test_ready_without_systemd(self):
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(io.StringIO()):
            asyncio.run(bot.on_ready())

    def test_ready_notifies_systemd(self):
        async def notify():
            with patch.dict(os.environ, {"NOTIFY_SOCKET": "/run/systemd/notify"}), \
                    patch("bot.socket.socket") as factory, \
                    contextlib.redirect_stdout(io.StringIO()):
                await bot.on_ready()
                client = factory.return_value.__enter__.return_value
                client.connect.assert_called_once_with("/run/systemd/notify")
                client.sendall.assert_called_once_with(b"READY=1")
        asyncio.run(notify())

    def test_ready_handles_abstract_systemd_socket(self):
        async def notify():
            with patch.dict(os.environ, {"NOTIFY_SOCKET": "@notify"}), \
                    patch("bot.socket.socket") as factory, \
                    contextlib.redirect_stdout(io.StringIO()):
                await bot.on_ready()
                factory.return_value.__enter__.return_value.connect.assert_called_once_with("\0notify")
        asyncio.run(notify())
