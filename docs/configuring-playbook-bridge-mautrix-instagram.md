# Setting up Mautrix Instagram (optional)

The playbook can install and configure [mautrix-instagram](https://github.com/tulir/mautrix-instagram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/instagram/index.html) to learn what it does and why it might be useful to you.

```yaml
matrix_mautrix_instagram_enabled: true
```

## Usage

You then need to start a chat with `@instagrambot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

Send `login YOUR_INSTAGRAM_EMAIL_ADDRESS YOUR_INSTAGRAM_PASSWORD` to the bridge bot to enable bridging for your instagram/Messenger account.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/instagram/authentication.html).
