<!--
SPDX-FileCopyrightText: 2020 Scott Crossen
SPDX-FileCopyrightText: 2020 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Dynamic DNS (optional)

The playbook can configure Dynamic DNS with [ddclient⁠](https://github.com/ddclient/ddclient) for you. It is a Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider.

Most cloud providers / ISPs will charge you extra for a static IP address. If you're not hosting a highly reliable homeserver you can workaround this via dynamic DNS.

## Prerequisite

You'll need to authenticate with your DNS provider somehow, in most cases this is simply a username and password but can differ from provider to provider. Please consult with your providers documentation and the upstream [ddclient documentation](https://github.com/ddclient/ddclient/blob/main/ddclient.conf.in) to determine what you'll need to provide to authenticate.

## Adjusting the playbook configuration

To enable dynamic DNS, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_dynamic_dns_enabled: true

matrix_dynamic_dns_domain_configurations:
  - provider: example.net
    protocol: dyndn2
    username: YOUR_USERNAME_HERE
    password: YOUR_PASSWORD_HERE
    domain: "{{ matrix_domain }}"
```

Keep in mind that certain providers may require a different configuration of the `matrix_dynamic_dns_domain_configurations` variable, for provider specific examples see the [upstream documentation](https://github.com/ddclient/ddclient/blob/main/ddclient.conf.in).

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-dynamic-dns/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Additional Reading

Additional resources:

- https://matrix.org/docs/guides/free-small-matrix-server
- https://github.com/linuxserver/docker-ddclient

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-dynamic-dns`. However, due to an [upstream issue](https://github.com/linuxserver/docker-ddclient/issues/54#issuecomment-1153143132) the logging output is not always complete. For advanced debugging purposes running the `ddclient` tool outside of the container is useful via the following: `ddclient -file ./ddclient.conf -daemon=0 -debug -verbose -noquiet`.
