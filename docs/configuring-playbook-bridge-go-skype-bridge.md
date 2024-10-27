# Setting up Go Skype Bridge bridging (optional)

The playbook can install and configure [go-skype-bridge](https://github.com/kelaresg/go-skype-bridge) for you.

See the project page to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [Skype](https://www.skype.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_go_skype_bridge_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once the bot is enabled, you need to start a chat with `Skype bridge bot` with the handle `@skypebridgebot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `help` to the bot to see the commands available.
