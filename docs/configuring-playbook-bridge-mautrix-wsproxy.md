# Setting up Mautrix wsproxy (optional)

The playbook can install and configure [mautrix-wsproxy](https://github.com/mautrix/wsproxy) for you.

See the project's [documentation](https://github.com/mautrix/wsproxy#readme) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_wsproxy_enabled: true

matrix_mautrix_androidsms_appservice_token: 'secret token from bridge'
matrix_mautrix_androidsms_homeserver_token: 'secret token from bridge'
matrix_mautrix_imessage_appservice_token: 'secret token from bridge'
matrix_mautrix_imessage_homeserver_token: 'secret token from bridge'
matrix_mautrix_wsproxy_syncproxy_shared_secret: 'secret token from bridge'
```

Note that the tokens must match what is compiled into the [mautrix-imessage](https://github.com/mautrix/imessage) bridge running on your Mac or Android device.

### Adjusting the wsproxy URL

By default, this playbook installs wsproxy on the `wsproxy.` subdomain (`wsproxy.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_mautrix_wsproxy_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname
matrix_mautrix_wsproxy_hostname: wsproxy.example.com
```

## Adjusting DNS records

Once you've decided on the domain, **you may need to adjust your DNS** records to point the wsproxy domain to the Matrix server.

By default, you will need to create a CNAME record for `wsproxy`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Follow the [matrix-imessage documenation](https://docs.mau.fi/bridges/go/imessage/index.html) for running `android-sms` and/or `matrix-imessage` on your device(s).
