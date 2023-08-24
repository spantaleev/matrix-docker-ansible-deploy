# Setting up Mautrix wsproxy (optional)

The playbook can install and configure [mautrix-wsproxy](https://github.com/mautrix/wsproxy) for you.

See the project's [documentation](https://github.com/mautrix/wsproxy#readme) to learn what it does and why it might be useful to you.


## DNS

You need to create a `wsproxy.DOMAIN` DNS record pointing to your Matrix server (a `CNAME` pointing to `matrix.DOMAIN`) to use wsproxy.
The hostname is configurable via a `matrix_mautrix_wsproxy_hostname` variable.


## Configuration

Use the following playbook configuration:

```yaml
matrix_mautrix_wsproxy_enabled: true

matrix_mautrix_androidsms_appservice_token: 'secret token from bridge'
matrix_mautrix_androidsms_homeserver_token: 'secret token from bridge'
matrix_mautrix_imessage_appservice_token: 'secret token from bridge'
matrix_mautrix_imessage_homeserver_token: 'secret token from bridge'
matrix_mautrix_wsproxy_syncproxy_shared_secret: 'secret token from bridge'
```

Note that the tokens must match what is compiled into the [mautrix-imessage](https://github.com/mautrix/imessage) bridge running on your Mac or Android device.


## Usage

Follow the [matrix-imessage documenation](https://docs.mau.fi/bridges/go/imessage/index.html) for running `android-sms` and/or `matrix-imessage` on your device(s).
