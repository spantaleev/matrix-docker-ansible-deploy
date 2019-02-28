# Setting up Mautrix Telegram (optional)

The playbook can install and configure [mautrix-telegram](https://github.com/tulir/mautrix-telegram) for you.

See the project's [documentation](https://github.com/tulir/mautrix-telegram/wiki#usage) to learn what it does and why it might be useful to you.

You'll need to obtain API keys from `https://my.telegram.org/apps` and then use the following playbook configuration:

```yaml
matrix_mautrix_telegram_enabled: true
matrix_mautrix_telegram_api_id: YOUR_TELEGRAM_APP_ID
matrix_mautrix_telegram_api_hash: YOUR_TELEGRAM_API_HASH
```

You then need to start a chat with `@telegrambot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
