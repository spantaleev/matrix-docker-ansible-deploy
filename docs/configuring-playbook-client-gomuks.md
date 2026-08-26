<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up gomuks (optional)

The playbook can install and configure [gomuks](https://github.com/gomuks/gomuks) for you.

gomuks is a Matrix client written in Go. The `gomuks` container in this playbook runs the gomuks backend which serves the web frontend. It acts as a bouncer — keeping your encryption keys and syncing in the background, even when the browser is closed. See the project's [documentation](https://docs.mau.fi/gomuks/) to learn what it does and why it might be useful to you.

By default, this playbook does not install gomuks. Element Web remains the default client.

## Adjusting DNS records

By default, this playbook installs gomuks on the `gomuks.` subdomain (`gomuks.example.com`) and requires you to create a CNAME record for `gomuks`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable gomuks, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_gomuks_enabled: true
```

### Adjusting the gomuks URL (optional)

By tweaking the `matrix_client_gomuks_hostname` and `matrix_client_gomuks_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for gomuks.
matrix_client_gomuks_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /gomuks subpath
matrix_client_gomuks_path_prefix: /gomuks
```

After changing the domain, **you may need to adjust your DNS** records to point the gomuks domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

**Note**: `matrix_client_gomuks_path_prefix` must either be `/` or not end with a slash (e.g. `/gomuks`).

### Adjusting authentication (optional)

gomuks protects its web interface with a basic-auth username and password (separate from your Matrix account). The playbook auto-generates these from `matrix_homeserver_generic_secret_key`:

- `matrix_client_gomuks_auth_username` — defaults to `gomuks`
- `matrix_client_gomuks_auth_password` — auto-generated, truncated hash of the secret key

To set your own credentials, add the following to your `vars.yml`:

```yaml
matrix_client_gomuks_auth_username: "myuser"
matrix_client_gomuks_auth_password: "mysupersecretpassword"
```

The playbook derives a bcrypt hash automatically. You can also set the hash directly:

```yaml
matrix_client_gomuks_auth_password_hash: "$2a$12$..."
```

If your gomuks instance is behind an authenticating reverse proxy and you prefer to handle auth there, you can disable gomuks' own auth:

```yaml
matrix_client_gomuks_disable_auth: true
```

When disabling auth, be careful not to expose gomuks to untrusted networks. See the [gomuks FAQ](https://docs.mau.fi/gomuks/faq.html#can-i-run-the-backend-behind-a-reverse-proxy) for details.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-client-gomuks/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-client-gomuks/templates/config.yaml.j2` for the component's default runtime configuration. gomuks stores additional settings (like VAPID keys, `token_key`, etc.) in `/data/config/config.yaml`; the playbook generates them from your `matrix_homeserver_generic_secret_key` so that they remain stable across restarts

Additional useful variables include:

- `matrix_client_gomuks_container_image` — override the container image
- `matrix_client_gomuks_web_listen_address` — listen address inside the container
- `matrix_client_gomuks_origin_patterns` — allowed `Origin` header patterns
- `matrix_client_gomuks_insecure_cookies` — allow cookies over plain HTTP (useful without TLS, not recommended)

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

After installation, gomuks will be available at `https://gomuks.example.com` (or your custom hostname/path).

1. Open the URL in your browser.
2. You will be prompted for the gomuks basic-auth credentials (see [Adjusting authentication](#adjusting-authentication-optional)). This is **not** your Matrix password — it's the bouncer protection.
3. Log in with your Matrix account (user ID, password, homeserver).

Your encryption keys stay on the server's `/matrix/client-gomuks/data` directory, so the backend keeps syncing even when no browser is open.

All gomuks data (config, database, logs) lives under `{{ matrix_client_gomuks_data_path }}` (`/matrix/client-gomuks` by default) on the server.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-client-gomuks`.

If you changed `matrix_client_gomuks_auth_password` and cannot log in, note that the browser may have cached the old basic-auth credentials — try a private window or clear site data.

If you see errors about `origin_patterns`, verify that `matrix_client_gomuks_hostname` and `matrix_client_gomuks_origin_patterns` include the hostname you are using to access gomuks (without `https://` and with explicit port if non-standard).

To reset gomuks completely (removes database and forces re-login), stop the service and remove its data directory, then re-run the playbook:

```sh
systemctl stop matrix-client-gomuks
rm -rf /matrix/client-gomuks/data/*
# then re-run: just setup-all --tags=setup-client-gomuks
```
