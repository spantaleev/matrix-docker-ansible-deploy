# Setting up Mautrix wsproxy for bridging Android SMS or Apple iMessage (optional)

The playbook can install and configure [mautrix-wsproxy](https://github.com/mautrix/wsproxy) for you.

See the project's [documentation](https://github.com/mautrix/wsproxy/blob/master/README.md) to learn what it does and why it might be useful to you.

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
matrix_mautrix_wsproxy_hostname: ws.example.com
```

## Adjusting DNS records

Once you've decided on the domain, **you may need to adjust your DNS** records to point the wsproxy domain to the Matrix server.

By default, you will need to create a CNAME record for `wsproxy`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

Follow the [matrix-imessage documenation](https://docs.mau.fi/bridges/go/imessage/index.html) for running `android-sms` and/or `matrix-imessage` on your device(s).
