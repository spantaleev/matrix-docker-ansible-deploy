<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Matěj Cepl

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up gomuks (optional)

The playbook can install and configure [gomuks](https://github.com/gomuks/gomuks) for you.

gomuks is a Matrix client written in Go. The `gomuks` container runs the backend and serves the web frontend. The backend stores your encryption keys and continues syncing while the browser is closed. See the project's [documentation](https://docs.mau.fi/gomuks/) for more information.

By default, this playbook does not install gomuks. Element Web remains the default client.

## Adjusting DNS records

By default, this playbook installs gomuks on the `gomuks.` subdomain (`gomuks.example.com`) and requires you to create a CNAME record for `gomuks`, which targets `matrix.example.com`.

When creating the record, replace `example.com` with your own domain.

## Adjusting the playbook configuration

To enable gomuks, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_gomuks_enabled: true

# This protects the gomuks backend and is separate from your Matrix password.
matrix_client_gomuks_auth_password: "YOUR_STRONG_PASSWORD_HERE"
```

Replace `YOUR_STRONG_PASSWORD_HERE` with a strong password.

### Adjusting the gomuks URL (optional)

You can make the service available at a different hostname or path by changing `matrix_client_gomuks_hostname` and `matrix_client_gomuks_path_prefix`.

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

`matrix_client_gomuks_path_prefix` must either be `/` or not end with a slash, such as `/gomuks`.

### Configuring authentication

gomuks protects its web interface with a basic-auth username and password which are separate from your Matrix account. `matrix_client_gomuks_auth_username` defaults to `gomuks`. You must define `matrix_client_gomuks_auth_password` when enabling the service, unless you disable gomuks authentication as described below:

```yaml
matrix_client_gomuks_auth_username: "gomuks"
matrix_client_gomuks_auth_password: "YOUR_STRONG_PASSWORD_HERE"
```

The playbook stores only a bcrypt hash of this password in the gomuks configuration file.

If your gomuks instance is behind an authenticating reverse proxy and you prefer to handle authentication there, you can disable gomuks authentication:

```yaml
matrix_client_gomuks_disable_auth: true
```

`matrix_client_gomuks_auth_password` is not required when authentication is disabled. Be careful not to expose gomuks to untrusted networks. See the [gomuks FAQ](https://docs.mau.fi/gomuks/faq.html#can-i-run-the-backend-behind-a-reverse-proxy) for details.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-client-gomuks/defaults/main.yml` for variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-client-gomuks/templates/config.yaml.j2` for the default runtime configuration

By default, gomuks generates a VAPID key pair for Web Push on first startup. The playbook preserves this pair on later runs. You can instead supply a pair with `matrix_client_gomuks_push_vapid_private_key` and `matrix_client_gomuks_push_vapid_public_key`; both variables must be set together.

Other useful variables include:

- `matrix_client_gomuks_container_image` to override the container image
- `matrix_client_gomuks_web_listen_address` to change the listen address inside the container
- `matrix_client_gomuks_origin_patterns` to change the allowed `Origin` header patterns
- `matrix_client_gomuks_insecure_cookies` to allow cookies over plain HTTP, which is not recommended

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
2. Enter the gomuks basic-auth credentials described in [Configuring authentication](#configuring-authentication). These are not your Matrix credentials.
3. Log in with your Matrix account (user ID, password, homeserver).

Your encryption keys stay on the server's `/matrix/client-gomuks/data` directory, so the backend keeps syncing even when no browser is open.

The `matrix_client_gomuks_data_path` variable controls where gomuks stores its configuration, database, cache, and logs. Its default value is `/matrix/client-gomuks`. Disabling gomuks stops and removes the service but preserves this directory.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-client-gomuks`.

If you changed `matrix_client_gomuks_auth_password` and cannot log in, the browser may have cached the old basic-auth credentials. Try a private window or clear the site's data.

If you see errors about `origin_patterns`, verify that `matrix_client_gomuks_hostname` and `matrix_client_gomuks_origin_patterns` include the hostname you are using to access gomuks (without `https://` and with explicit port if non-standard).

To log out and remove the locally stored Matrix account state, stop the service and remove its data and cache directories. This preserves the gomuks configuration and VAPID keys:

```sh
systemctl stop matrix-client-gomuks
rm -rf /matrix/client-gomuks/data /matrix/client-gomuks/cache
just install-service client-gomuks
```
