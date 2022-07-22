# Setting up Matrix Appservice KakaoTalk (optional)

The playbook can install and configure
[matrix-appservice-kakaotalk](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [KakaoTalk](https://www.kakaocorp.com/page/service/service/KakaoTalk) bridge just use the following
playbook configuration:


```yaml
matrix_appservice_kakaotalk_enabled: true
```


## Usage

Once the bot is enabled, you need to start a chat with `KakaoTalk bridge bot`
with the handle `@kakaotalkbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Send `help` to the bot to see the commands available.
