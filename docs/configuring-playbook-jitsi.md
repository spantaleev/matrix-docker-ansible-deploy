<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the Jitsi video-conferencing platform (optional)

The playbook can install and configure the [Jitsi](https://jitsi.org/) video-conferencing platform for you.

Jitsi is an open source video-conferencing platform. It can not only be integrated with Element clients ([Element Web](configuring-playbook-client-element-web.md)/Desktop, Android and iOS) as a widget, but also be used as standalone web app.

💡 If you're into experimental technology, you may also be interested in trying out [Element Call](configuring-playbook-element-call.md) - a native Matrix video conferencing application.

The [Ansible role for Jitsi](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring Jitsi, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md) online
- 📁 `roles/galaxy/jitsi/docs/configuring-jitsi.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Prerequisites

Before proceeding, make sure to check server's requirements recommended by [the official deployment guide](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements).

You may need to open some ports to your server, if you use another firewall in front of the server. Refer [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#prerequisites) to check which ones to be configured.

## Adjusting DNS records

By default, this playbook installs Jitsi on the `jitsi.` subdomain (`jitsi.example.com`) and requires you to create a CNAME record for `jitsi`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Jitsi, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
########################################################################
#                                                                      #
# jitsi                                                                #
#                                                                      #
########################################################################

jitsi_enabled: true

########################################################################
#                                                                      #
# /jitsi                                                               #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable Jitsi on your Matrix server with this minimum configuration.

However, **since Jitsi's performance heavily depends on server resource (bandwidth, RAM, and CPU), it is recommended to review settings and optimize them as necessary before deployment.** You can check [here](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#example-configurations) for an example set of configurations to set up a Jitsi instance, focusing on performance. If you will host a large conference, you probably might also want to consider to provision additional JVBs ([Jitsi VideoBridge](https://github.com/jitsi/jitsi-videobridge)). See [here](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#set-up-additional-jvbs-for-more-video-conferences-optional) for details about setting them up with the playbook.

See the role's documentation for details about configuring Jitsi per your preference (such as setting [a custom hostname](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#set-the-hostname) and [the environment variable for running Jitsi in a LAN](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#configure-jvb_advertise_ips-for-running-behind-nat-or-on-a-lan-environment-optional)).

### Enable authentication and guests mode (optional)

By default the Jitsi Meet instance **does not require for anyone to log in, and is open to use without an account**.

If you would like to control who is allowed to start meetings on your instance, you'd need to enable Jitsi's authentication and optionally guests mode.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#configure-jitsi-authentication-and-guests-mode-optional) on the role's documentation for details about how to configure the authentication and guests mode. The recommended authentication method is `internal` as it also works in federated rooms. If you want to enable authentication with Matrix OpenID making use of [Matrix User Verification Service (UVS)](configuring-playbook-user-verification-service.md), see [here](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#authenticate-using-matrix-openid-auth-type-matrix) for details about how to set it up.

### Enable Gravatar (optional)

In the default Jisti Meet configuration, `gravatar.com` is enabled as an avatar service.

Since the Element clients send the URL of configured Matrix avatars to the Jitsi instance, our configuration has disabled the Gravatar service.

To enable the Gravatar service nevertheless, add the following configuration to your `vars.yml` file:

```yaml
jitsi_disable_gravatar: false
```

> [!WARNING]
> This will result in third party request leaking data to the Gravatar Service (`gravatar.com`, unless configured otherwise). Besides metadata, the Matrix user_id and possibly the room ID (via `referrer` header) will be also sent to the third party.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

You can use the self-hosted Jitsi server in multiple ways:

- **by adding a widget to a room via Element Web** (the one configured by the playbook at `https://element.example.com`). Just start a voice or a video call in a room containing more than 2 members and that would create a Jitsi widget which utilizes your self-hosted Jitsi server.

- **directly (without any Matrix integration)**. Just go to `https://jitsi.example.com`, and you can start a videoconference.

Note that you'll need to log in to your Jitsi's account to start a conference if you have configured authentication with `internal` auth.

Check [the official user guide](https://jitsi.github.io/handbook/docs/category/user-guide) for details about how to use Jitsi.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#troubleshooting) on the role's documentation for details.
