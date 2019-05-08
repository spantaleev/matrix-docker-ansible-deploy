# Setting up Mautrix Facebook (optional)

The playbook can install and configure [mautrix-facebook](https://github.com/tulir/mautrix-facebook) for you.

See the project's [documentation](https://github.com/tulir/mautrix-facebook/wiki#usage) to learn what it does and why it might be useful to you.

```yaml
matrix_mautrix_facebook_enabled: true
```

You then need to start a chat with `@facebookbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
