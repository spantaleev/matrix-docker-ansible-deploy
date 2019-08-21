# Setting up Mautrix Hangouts (optional)

The playbook can install and configure [mautrix-hangouts](https://github.com/tulir/mautrix-hangouts) for you.

See the project's [documentation](https://github.com/tulir/mautrix-hangouts/wiki#usage) to learn what it does and why it might be useful to you.

To enable the [Google Hangouts](https://hangouts.google.com/) bridge just use the following playbook configuration:


```yaml
matrix_mautrix_hangouts_enabled: true
```

## Usage

Once the bot is enabled you need to start a chat with `Hangouts bridge bot` with handle `@hangoutsbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

Send `login` to the bridge bot to receive a link to the portal from which you can enable the bridging. Open the link sent by the bot and follow the instructions.

Automatic login may not work. If it does not, reload the page and select the "Manual login" checkbox before starting. Manual login involves logging into your Google account normally and then manually getting the OAuth token from browser cookies with developer tools.

Once logged in, recent chats should show up as new conversations automatically. Other chats will get portals as you receive messages.

You can learn more about authentication from the bridge's [official documentation on Authentication](https://github.com/tulir/mautrix-hangouts/wiki/Authentication).
