"""Exercise real command parsing and Discord message serialization offline."""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from discord.ext import commands
from discord.http import Route

import bot
from local_bot import mock_discord


class LocalBotTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        session = mock_discord(bot.bot)
        self.api = await session.__aenter__()
        self.addAsyncCleanup(session.__aexit__, None, None, None)

    async def send(self, content, **kwargs):
        await self.api.send(content, **kwargs)
        self.assertEqual(self.api.errors, [])
        return self.api.replies[-1]

    async def test_version_serializes_reply_reference(self):
        reply = await self.send("z!version")
        self.assertIn(bot.ver, reply["content"])
        self.assertEqual(reply["message_reference"]["message_id"], 1001)
        self.assertEqual(self.api.requests, [("POST", "/channels/{channel_id}/messages")])

    async def test_help_embed_lists_visible_commands(self):
        reply = await self.send("z!help")
        embed = reply["embeds"][0]
        self.assertEqual(embed["color"], bot.gubbycolour)
        names = {field["name"] for field in embed["fields"]}
        self.assertIn("z!trans", names)
        self.assertIn("z!sing", names)
        self.assertNotIn("z!xomer", names)
        reply = await self.send("z!help trans")
        self.assertEqual(reply["embeds"][0]["description"], bot.trans.help)

    async def test_translation_fetches_referenced_message(self):
        original = self.api.message("Hello to the gubby!")
        with patch("bot.randint", return_value=1):
            reply = await self.send("z!trans", reply_to=original.id)
        self.assertEqual(reply["content"], "h3ll0 2 d4 gubb3h! :3")
        self.assertEqual(self.api.requests[0], ("GET", "/channels/{channel_id}/messages/{message_id}"))

    async def test_translation_without_reply(self):
        reply = await self.send("z!trans")
        self.assertIn("d1dn't r3ply", reply["content"])

    async def test_translation_fetch_failures(self):
        for status, expected in [(404, "d3l3t3d"), (500, "f41l3d")]:
            with self.subTest(status=status), contextlib.redirect_stdout(io.StringIO()) as output:
                self.api.fetch_status = status
                await self.api.send("z!trans", reply_to=9999)
                self.assertIn(expected, output.getvalue())
                self.assertEqual(self.api.replies, [])
                self.assertEqual(self.api.errors, [])

    async def test_sing_argument_parsing_and_fallbacks(self):
        for content, expected in [
            ("z!sing", "r3m3mb3r"),
            ("z!sing + homer let the barts out outro", "d4 d00r 1z 0p3n"),
            ("z!sing + gubby unknown", "d0nt kn0w"),
            ("z!sing unknown", "d0n't kn0w"),
        ]:
            with self.subTest(content=content):
                reply = await self.send(content)
                self.assertIn(expected, reply["content"])
        with patch("bot.choice", return_value="outro") as choose:
            reply = await self.send("z!sing homer")
        choose.assert_called_once()
        self.assertIn("d4 d00r 1z 0p3n", reply["content"])

    async def test_pet_changelog_and_username(self):
        with patch("bot.randint", return_value=1):
            self.assertEqual((await self.send("z!pet"))["content"], ":3")
        self.assertIn("z0.7.1", (await self.send("z!changelog z0.7.1"))["content"])
        self.assertIn("1nv4l1d", (await self.send("z!changelog unknown"))["content"])
        self.assertEqual((await self.send("z!xomer"))["content"], "l4rp.")
        self.assertIn("h3ll0 z9", (await self.send("z!xomer", username="z9xomer"))["content"])

    async def test_non_commands_and_bot_messages_are_ignored(self):
        await self.api.send("hello")
        await self.api.send("z!version", author_bot=True)
        self.assertEqual(self.api.replies, [])
        self.assertEqual(self.api.requests, [])

    async def test_unknown_command_and_bad_arguments_are_visible(self):
        await self.api.send("z!unknown")
        self.assertIsInstance(self.api.errors[-1], commands.CommandNotFound)
        await self.api.send('z!sing "unclosed')
        self.assertIsInstance(self.api.errors[-1], commands.ExpectedClosingQuoteError)

    async def test_unmocked_api_and_gateway_calls_fail_locally(self):
        with self.assertRaisesRegex(RuntimeError, "Unmocked Discord route"):
            await bot.bot.http.request(Route("GET", "/users/@me"))
        with self.assertRaisesRegex(RuntimeError, "Login disabled"):
            await bot.bot.login("not-a-token")
        with self.assertRaisesRegex(RuntimeError, "Gateway disabled"):
            await bot.bot.connect()


class LocalCliTests(unittest.TestCase):
    def run_cli(self, *args, input=None):
        return subprocess.run(
            [sys.executable, str(Path(bot.__file__).with_name("local_bot.py")), *args],
            input=input, capture_output=True, text=True, timeout=15,
            env=dict(os.environ, DISCORD_TOKEN="", PYTHON_DOTENV_DISABLED="1"),
        )

    def test_scripted_session_without_token(self):
        result = self.run_cli("-m", "z!version", "-m", "z!help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(bot.ver, result.stdout)
        self.assertIn("z!trans:", result.stdout)

    def test_reply_option(self):
        result = self.run_cli("--seed", "1", "--reply-to", "Hello to the gubby!", "-m", "z!trans")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("h3ll0 2 d4 gubb3h!", result.stdout)

    def test_interactive_reply(self):
        result = self.run_cli(input="Hello gubby\n/reply 1001 z!trans\n/quit\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("h3ll0 gubb3h", result.stdout)

    def test_command_error_returns_failure_status(self):
        result = self.run_cli("-m", "z!unknown")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Command error:", result.stdout)
