<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Béla Becker
SPDX-FileCopyrightText: 2021 pushytoxin
SPDX-FileCopyrightText: 2022 Jim Myhrberg
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2022 felixx9
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Etherpad (optional)

The playbook can install and configure [Etherpad](https://etherpad.org) for you.

Etherpad is an open source collaborative text editor. It can not only be integrated with Element clients ([Element Web](configuring-playbook-client-element-web.md)/Desktop, Android and iOS) as a widget, but also be used as standalone web app.

When enabled together with the Jitsi video-conferencing platform (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.

The [Ansible role for Etherpad](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring Etherpad, you can check them via:

- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md) online
- 📁 `roles/galaxy/etherpad/docs/configuring-etherpad.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Adjusting DNS records

By default, this playbook installs Etherpad on the `etherpad.` subdomain (`etherpad.example.com`) and requires you to create a CNAME record for `etherpad`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Etherpad, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
########################################################################
#                                                                      #
# etherpad                                                             #
#                                                                      #
########################################################################

etherpad_enabled: true

########################################################################
#                                                                      #
# /etherpad                                                            #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Etherpad on your Matrix server with this minimum configuration.

See the role's documentation for details about configuring Etherpad per your preference (such as [the name of the instance](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#set-the-name-of-the-instance-optional) and [the default pad text](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#set-the-default-text-optional)).

### Create admin user (optional)

You probably might want to enable authentication to disallow anonymous access to your Etherpad.

It is possible to enable HTTP basic authentication by **creating an admin user** with `etherpad_admin_username` and `etherpad_admin_password` variables. The admin user account is also used by plugins for authentication and authorization.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#create-admin-user-optional) on the role's documentation for details about how to create the admin user.

### Adjusting the Etherpad URL (optional)

By tweaking the `etherpad_hostname` and `etherpad_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Etherpad.
etherpad_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /etherpad subpath
etherpad_path_prefix: /etherpad
```

After changing the domain, **you may need to adjust your DNS** records to point the Etherpad domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

By default, the Etherpad UI should be available at `https://etherpad.example.com`, while the admin UI (if enabled) should then be available at `https://etherpad.example.com/admin`.

If you've [decided on another hostname or path-prefix](#adjusting-the-etherpad-url-optional) (e.g. `https://matrix.example.com/etherpad`), adjust these URLs accordingly before using it.

💡 For more information about usage, take a look at [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#usage) on the role's documentation.

### Integrating a Etherpad widget in a room

**Note**: this is how it works in Element Web. It might work quite similar with other clients:

To integrate a standalone Etherpad in a room, create your pad by visiting `https://etherpad.example.com`. When the pad opens, copy the URL and send a command like this to the room: `/addwidget URL`. You will then find your integrated Etherpad within the right sidebar in the `Widgets` section.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#troubleshooting) on the role's documentation for details.
