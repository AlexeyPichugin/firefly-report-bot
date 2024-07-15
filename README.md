# firefly-report-bot

## Setup

1. Create settings file
```shell
cp settings_example.yaml settings.yaml
```

2. Edit settings file
You need to set:
- firefly.api_key - The API key for the Firefly client
- firefly.api_url - The API URL for the Firefly client
- telegram.bot_token - The token for the Telegram bot
- telegram.chat_id - The chat ID for the Telegram bot

Other params is not required

3. Run bot in docker
```shell
docker run \
  --rm --it --init --name firefly-bot \
  --volume /srv/app/settings.yaml:$(pwd)/settings.yaml:ro \
  apichugin/firefly-report-bot:latest
```