# Setting up the WeChat Bridge (optional)

The playbook can install and configure the [matrix-wechat](https://github.com/duo/matrix-wechat) bridge for you (for bridging to the [WeChat](https://www.wechat.com/) network).

See the project page to learn what it does and why it might be useful to you.

To enable the bridge, use the following playbook configuration and re-run the playbook's [installation](./installing.md) procedure:

```yaml
matrix_wechat_enabled: true
```

## Usage

Once the bridge is installed, start a chat with `@wechatbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

Send `help` to the bot to see the available commands.
