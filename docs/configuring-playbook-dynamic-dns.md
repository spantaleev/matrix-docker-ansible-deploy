<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Scott Crossen
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Dynamic DNS (optional)

The playbook can configure Dynamic DNS with [ddclient⁠](https://github.com/ddclient/ddclient) for you. It is a Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider.

Most cloud providers / ISPs will charge you extra for a static IP address. If you're not hosting a highly reliable homeserver you can workaround this via dynamic DNS.

For details about configuring the [Ansible role for ddclient](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient), you can check them via:
- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md) online
- 📁 `roles/galaxy/ddclient/docs/configuring-ddclient.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Prerequisite

You'll need to authenticate with your DNS provider somehow, in most cases this is simply a username and password but can differ from provider to provider. Please consult with your providers documentation and the upstream [ddclient documentation](https://github.com/ddclient/ddclient/blob/main/ddclient.conf.in) to determine what you'll need to provide to authenticate.

## Adjusting the playbook configuration

To enable dynamic DNS, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
ddclient_enabled: true

ddclient_domain_configurations:
  - provider: example.net
    protocol: dyndns2
    username: YOUR_USERNAME_HERE
    password: YOUR_PASSWORD_HERE
    domain: "{{ matrix_domain }}"
```

Keep in mind that certain providers may require a different configuration of the `ddclient_domain_configurations` variable, for provider specific examples see the [upstream documentation](https://github.com/ddclient/ddclient/blob/main/ddclient.conf.in).

### Configuring the endpoint to obtain IP address (optional)

The playbook sets the default endpoint for obtaining the IP address to `https://cloudflare.com/cdn-cgi/trace`. You can replace it by specifying yours to `ddclient_web` and `ddclient_web_skip` if necessary.

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md#setting-the-endpoint-to-obtain-ip-address-optional) for more information.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/galaxy/ddclient/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

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

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ddclient/blob/main/docs/configuring-ddclient.md#troubleshooting) on the role's documentation for details.
