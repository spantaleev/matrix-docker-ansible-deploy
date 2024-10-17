# Setting up the WeChat Bridge (optional)

The playbook can install and configure the [matrix-wechat](https://github.com/duo/matrix-wechat) bridge for you (for bridging to the [WeChat](https://www.wechat.com/) network).

See the project page to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_wechat_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once the bridge is installed, start a chat with `@wechatbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `help` to the bot to see the available commands.
