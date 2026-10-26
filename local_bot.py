"""Run the real bot against an in-memory Discord HTTP API, without logging in."""

import argparse
import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy
import random
from types import SimpleNamespace
from unittest.mock import patch

import discord


BOT_USER = {"id": "100", "username": "gubby", "discriminator": "0", "avatar": None, "bot": True}
CHANNEL_ID = 200


class MockDiscord:
    """Minimal message API for this bot; unsupported routes fail locally."""

    def __init__(self, client):
        self.client = client
        self.messages = {}
        self.replies = []
        self.errors = []
        self.requests = []
        self.fetch_status = None
        self._next_id = 1000
        self.channel = discord.DMChannel(
            me=client.user,
            state=client._connection,
            data={"id": str(CHANNEL_ID), "type": 1, "recipients": []},
        )

    def message(self, content, *, username="local-user", reply_to=None, author_bot=False):
        """Store a message without delivering it to the bot."""
        self._next_id += 1
        data = {
            "id": str(self._next_id),
            "channel_id": str(CHANNEL_ID),
            "author": {
                "id": "101", "username": username,
                "discriminator": "0", "avatar": None, "bot": author_bot,
            },
            "content": content,
            "timestamp": "2026-01-01T00:00:00+00:00",
            "edited_timestamp": None,
            "type": 0,
            "tts": False,
            "pinned": False,
            "mention_everyone": False,
            "mentions": [],
            "mention_roles": [],
            "attachments": [],
            "embeds": [],
        }
        if reply_to is not None:
            data["type"] = 19
            data["message_reference"] = {
                "message_id": str(reply_to), "channel_id": str(CHANNEL_ID),
            }
        self.messages[self._next_id] = data
        return discord.Message(state=self.client._connection, channel=self.channel, data=data)

    async def send(self, content, **kwargs):
        """Deliver a synthetic Discord message through the real on_message handler."""
        message = self.message(content, **kwargs)
        await self.client.on_message(message)
        return message

    async def request(self, route, **kwargs):
        self.requests.append((route.method, route.path))
        if route.channel_id != CHANNEL_ID:
            raise RuntimeError(f"Unmocked Discord route: {route.method} {route.path}")
        if route.method == "POST" and route.path == "/channels/{channel_id}/messages":
            payload = kwargs["json"]
            message = self.message(payload.get("content") or "", author_bot=True)
            data = self.messages[message.id]
            data.update(deepcopy(payload))
            data["author"] = dict(BOT_USER)
            if "message_reference" in payload:
                data["type"] = 19
            self.replies.append(deepcopy(data))
            return deepcopy(data)
        if route.method == "GET" and route.path == "/channels/{channel_id}/messages/{message_id}":
            message_id = int(route.url.rsplit("/", 1)[1])
            status = self.fetch_status or (404 if message_id not in self.messages else None)
            if status:
                response = SimpleNamespace(status=status, reason="Mock Discord error")
                error = discord.NotFound if status == 404 else discord.HTTPException
                raise error(response, {"code": 10008 if status == 404 else 0, "message": "Mock fetch failed"})
            return deepcopy(self.messages[message_id])
        raise RuntimeError(f"Unmocked Discord route: {route.method} {route.path}")


@asynccontextmanager
async def mock_discord(client):
    """Initialize discord.py locally and restore all mocks when the session ends.

    This uses discord.py internals for synthetic state; keep it tested when updating
    the pinned dependency. Never share this client with a live Discord session.
    """
    if client.is_closed():
        client.clear()
    async with client:
        user = discord.ClientUser(state=client._connection, data=BOT_USER)
        with patch.object(client._connection, "user", user):
            api = MockDiscord(client)
            original_dispatch = client.dispatch

            def dispatch(event, *args, **kwargs):
                if event == "command_error":
                    api.errors.append(args[1])
                else:
                    original_dispatch(event, *args, **kwargs)

            with patch.object(client.http, "request", side_effect=api.request), \
                    patch.object(client, "login", side_effect=RuntimeError("Login disabled in local mode")), \
                    patch.object(client, "connect", side_effect=RuntimeError("Gateway disabled in local mode")), \
                    patch.object(client, "dispatch", side_effect=dispatch):
                yield api


def show_message(data):
    print(f"[{data['id']}] {data['author']['username']}: {data.get('content', '')}")
    for embed in data.get("embeds", []):
        print(f"  {embed.get('title', '')}")
        if embed.get("description"):
            print(f"  {embed['description']}")
        for field in embed.get("fields", []):
            print(f"  {field['name']}: {field['value']}")


async def run(args):
    from bot import bot

    if args.seed is not None:
        random.seed(args.seed)
    async with mock_discord(bot) as api:
        reply_to = None
        if args.reply_to is not None:
            original = api.message(args.reply_to, username=args.username)
            reply_to = original.id
            show_message(api.messages[original.id])

        async def deliver(content, reference=None):
            start = len(api.replies)
            errors = len(api.errors)
            message = await api.send(content, username=args.username, reply_to=reference)
            show_message(api.messages[message.id])
            for reply in api.replies[start:]:
                show_message(reply)
            for error in api.errors[errors:]:
                print(f"Command error: {error}")

        if args.message:
            for content in args.message:
                await deliver(content, reply_to)
        else:
            print("Local Discord mock. Type z!help, /reply ID z!trans, or /quit.")
            while True:
                try:
                    content = input("> ")
                except EOFError:
                    break
                if content.strip() == "/quit":
                    break
                if content.startswith("/reply "):
                    parts = content.split(maxsplit=2)
                    if len(parts) != 3 or not parts[1].isdigit():
                        print("Usage: /reply ID message")
                        continue
                    await deliver(parts[2], int(parts[1]))
                else:
                    await deliver(content)
        return 1 if api.errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-m", "--message", action="append", help="Message to send; repeat for a scripted session")
    parser.add_argument("--reply-to", help="Original message text to reply to (requires --message)")
    parser.add_argument("--username", default="local-user", help="Simulated Discord username")
    parser.add_argument("--seed", type=int, help="Seed random replies for repeatable sessions")
    args = parser.parse_args()
    if args.reply_to is not None and not args.message:
        parser.error("--reply-to requires --message")
    try:
        return asyncio.run(run(args))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
