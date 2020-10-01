# telepinboard
Telegram bot for pushing bookmarks to Pinboard

## Usage

Set the following environment variables:
- `PB_TOKEN` - Pinboard API token.
- `TELEGRAM_USER` - Telegram user ID that will be allowed to communicate
                    with the bot.
- `TELEGRAM_TOKEN` - Telegram bot token.

Then run the script. Any text message containing a URL from the authorized
user will be processed by the bot. A new bookmark will be added to Pinboard
with the URL from the message and the title being the rest of the message text.
