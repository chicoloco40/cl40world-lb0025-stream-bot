CL40 World Stream Bot

Setup

1. Create `.env` in the project root with the bot token:

	DISCORD_TOKEN=your_token_here

2. (Optional) Set `BOT_SETTINGS_FILE` to change where runtime settings are stored.

Install and run

```bash
python3 -m pip install -r requirements.txt
python3 bot.py
```

Admin commands

- `!golive` - send official live embed (admin only)
- `!announce #channel` - send live embed to a channel (admin only)
- `!announce_album Title | https://link | note` - announce album release (admin only)
- `!exempt @user [days]` - temporary exempt user from spam/cooldown (default 3 days)
- `!unexempt @user` - remove temporary exemption
- `!setchannel #channel` - allow commands in a specific channel
- `!shutdown` - stop the bot

Notes

- The bot persists `allowed_channels` and `exempt_runtime` to `settings.json` by default.
- Keep your `.env` secret. Add it to `.gitignore` to avoid leaking the token.
