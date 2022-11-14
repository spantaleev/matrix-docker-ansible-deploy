# Setting up Go Skype Bridge (optional)

The playbook can install and configure
[go-skype-bridge](https://github.com/kelaresg/go-skype-bridge) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [Skype](https://www.skype.com/) bridge just use the following
playbook configuration:


```yaml
matrix_go_skype_bridge_enabled: true
```


## Usage

Once the bot is enabled, you need to start a chat with `Skype bridge bot`
with the handle `@skypebridgebot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Send `help` to the bot to see the commands available.
