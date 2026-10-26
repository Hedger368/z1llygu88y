# z1llygu88y

Discord gubby bot, using Python 3.10+.

## Local testing with a mocked Discord API

Install the dependencies once:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start an interactive local session:

```sh
python local_bot.py
```

Type commands such as `z!help`, `z!version`, `z!pet`, or
`z!sing + gubby chorus`. Messages and bot replies are printed with IDs.
To test translation, type a normal message, then reply to its ID:

```text
> Hello to the gubby!
[1001] local-user: Hello to the gubby!
> /reply 1001 z!trans
```

Use `/quit` or Ctrl-D to exit. You can also run commands directly:

```sh
python local_bot.py -m 'z!version' -m 'z!help'
python local_bot.py --seed 1 --reply-to 'Hello to the gubby!' -m 'z!trans'
python local_bot.py --username z9xomer -m 'z!xomer'
```

`--seed` makes random replies repeatable. Command errors print to the terminal
and produce exit status 1. No Discord token, server, or `.env` file is needed.
The runner uses the actual bot, message objects, command parser, and reply
serialization, with an in-memory mock of Discord's send/fetch message HTTP
endpoints. Login, gateway connections, and unsupported API routes fail locally.
It does not emulate Discord permissions, rate limits, gateway events, or embed
rendering; those still need testing against Discord.

Run the offline bot tests (standard-library `unittest`, no extra test packages):

```sh
python -m unittest discover -s tests -p 'test*bot.py' -v
```

On Linux, run the full suite including the deployment shell tests:

```sh
python -m unittest discover -s tests -v
```

## Connecting to Discord

Copy `.env.example` to `.env`, set `DISCORD_TOKEN`, and run `python bot.py`.
This starts the real Discord connection; use `local_bot.py` for offline testing.
