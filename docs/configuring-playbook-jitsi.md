<!--
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
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

The Ansible role for Jitsi is developed and maintained by [MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi). For details about configuring Jitsi, you can check them via:
- [the role's document at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md)
- `roles/galaxy/jitsi/docs/configuring-jitsi.md` locally, if you have fetched the Ansible roles

## Prerequisites

Before proceeding, make sure to check server's requirements recommended by [the official deployment guide](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements).

You may need to open some ports to your server, if you use another firewall in front of the server. Refer [the role's document](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#prerequisites) to check which ones to be configured.

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

See the role's document for details about configuring Jitsi per your preference (such as setting [a custom hostname](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#set-the-hostname) and [the environment variable for running Jitsi in a LAN](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#configure-jvb_advertise_ips-for-running-behind-nat-or-on-a-lan-environment-optional)).

### Enable authentication and guests mode (optional)

By default the Jitsi Meet instance **does not require for anyone to log in, and is open to use without an account**.

If you would like to control who is allowed to start meetings on your instance, you'd need to enable Jitsi's authentication and optionally guests mode.

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#configure-jitsi-authentication-and-guests-mode-optional) on the role's document for details about how to configure the authentication and guests mode. The recommended authentication method is `internal` as it also works in federated rooms. If you want to enable authentication with Matrix OpenID making use of [Matrix User Verification Service (UVS)](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-user-verification-service.md), see [here](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md#authenticate-using-matrix-openid-auth-type-matrix) for details about how to set it up.

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

### Set up additional JVBs for more video-conferences (optional)

By default, a single JVB ([Jitsi VideoBridge](https://github.com/jitsi/jitsi-videobridge)) is deployed on the same host as the Matrix server. To allow more video-conferences to happen at the same time, you'd need to provision additional JVB services on other hosts.

These settings below will allow you to provision those extra JVB instances. The instances will register themselves with the Prosody service, and be available for Jicofo to route conferences too.

#### Add the `jitsi_jvb_servers` section on `hosts` file

For additional JVBs, you'd need to add the section titled `jitsi_jvb_servers` on the ansible `hosts` file with the details of the JVB hosts as below:

```INI
[jitsi_jvb_servers]
jvb-2.example.com ansible_host=192.168.0.2
```

Make sure to replace `jvb-2.example.com` with your hostname for the JVB and `192.168.0.2` with your JVB's external IP address, respectively.

You could add JVB hosts as many as you would like. When doing so, add lines with the details of them.

#### Prepare `vars.yml` files for additional JVBs

If the main server is `matrix.example.com` and the additional JVB instance is going to be deployed at `jvb-2.example.com`, the variables for the latter need to be specified on `vars.yml` in its directory (`inventory/host_vars/jvb-2.example.com`).

Note that most (if not all) variables are common for both servers.

If you are setting up multiple JVB instances, you'd need to create `vars.yml` files for each of them too (`inventory/host_vars/jvb-3.example.com/vars.yml`, for example).

#### Set the server ID to each JVB

Each JVB requires a server ID to be set, so that it will be uniquely identified. The server ID allows Jitsi to keep track of which conferences are on which JVB.

The server ID can be set with the variable `jitsi_jvb_server_id`. It will end up as the `JVB_WS_SERVER_ID` environment variables in the JVB docker container.

To set the server ID to `jvb-2`, add the following configuration to either `hosts` or `vars.yml` files (adapt to your needs).

- On `hosts`:

  Add `jitsi_jvb_server_id=jvb-2` after your JVB's external IP addresses as below:

  ```INI
  [jitsi_jvb_servers]
  jvb-2.example.com ansible_host=192.168.0.2 jitsi_jvb_server_id=jvb-2
  jvb-3.example.com ansible_host=192.168.0.3 jitsi_jvb_server_id=jvb-2
  ```

- On `vars.yml` files:

  ```yaml
  jitsi_jvb_server_id: 'jvb-2'
  ```

Alternatively, you can specify the variable as a parameter to [the ansible command](#run-the-playbook).

**Note**: the server ID `jvb-1` is reserved for the JVB instance running on the Matrix host, therefore should not be used as the ID of an additional JVB host.

#### Set colibri WebSocket port

The additional JVBs will need to expose the colibri WebSocket port.

To expose the port, add the following configuration to your `vars.yml` files:

```yaml
jitsi_jvb_container_colibri_ws_host_bind_port: 9090
```

#### Set Prosody XMPP server

The JVB will also need to know the location of the Prosody XMPP server.

Similar to the server ID (`jitsi_jvb_server_id`), this can be set with the variable for the JVB by using the variable `jitsi_xmpp_server`.

##### Set the Matrix domain

The Jitsi Prosody container is deployed on the Matrix server by default, so the value can be set to the Matrix domain. To set the value, add the following configuration to your `vars.yml` files:

```yaml
jitsi_xmpp_server: "{{ matrix_domain }}"
```

##### Set an IP address of the Matrix server

Alternatively, the IP address of the Matrix server can be set. This can be useful if you would like to use a private IP address.

To set the IP address of the Matrix server, add the following configuration to your `vars.yml` files:

```yaml
jitsi_xmpp_server: "192.168.0.1"
```

##### Expose XMPP port

By default, the Matrix server does not expose the XMPP port (`5222`); only the XMPP container exposes it internally inside the host. This means that the first JVB (which runs on the Matrix server) can reach it but the additional JVBs cannot. Therefore, the XMPP server needs to expose the port, so that the additional JVBs can connect to it.

To expose the port and have Docker forward the port, add the following configuration to your `vars.yml` files:

```yaml
jitsi_prosody_container_jvb_host_bind_port: 5222
```

#### Reverse-proxy with Traefik

To make Traefik reverse-proxy to these additional JVBs, add the following configuration to your main `vars.yml` file (`inventory/host_vars/matrix.example.com/vars.yml`):

```yaml
# Traefik proxying for additional JVBs. These can't be configured using Docker
# labels, like the first JVB is, because they run on different hosts, so we add
# the necessary configuration to the file provider.
traefik_provider_configuration_extension_yaml: |
  http:
   routers:
     {% for host in groups['jitsi_jvb_servers'] %}

     additional-{{ hostvars[host]['jitsi_jvb_server_id'] }}-router:
       entryPoints:
         - "{{ traefik_entrypoint_primary }}"
       rule: "Host(`{{ jitsi_hostname }}`) && PathPrefix(`/colibri-ws/{{ hostvars[host]['jitsi_jvb_server_id'] }}/`)"
       service: additional-{{ hostvars[host]['jitsi_jvb_server_id'] }}-service
       {% if traefik_entrypoint_primary != 'web' %}

       tls:
         certResolver: "{{ traefik_certResolver_primary }}"

       {% endif %}

     {% endfor %}

   services:
     {% for host in groups['jitsi_jvb_servers'] %}

     additional-{{ hostvars[host]['jitsi_jvb_server_id'] }}-service:
       loadBalancer:
         servers:
           - url: "http://{{ host }}:9090/"

     {% endfor %}
```

#### Run the playbook

After configuring `hosts` and `vars.yml` files, run the playbook with [playbook tags](playbook-tags.md) as below:

```sh
ansible-playbook -i inventory/hosts --limit jitsi_jvb_servers jitsi_jvb.yml --tags=common,setup-additional-jitsi-jvb,start
```

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running the commands below:
- `journalctl -fu matrix-jitsi-web`
- `journalctl -fu matrix-jitsi-prosody`
- `journalctl -fu matrix-jitsi-jicofo`
- `journalctl -fu matrix-jitsi-jvb`

### `Error: Account creation/modification not supported`

If you get an error like `Error: Account creation/modification not supported` with authentication enabled, it's likely that you had previously installed Jitsi without auth/guest support.

In this case, you should consider to rebuild your Jitsi installation.

### Rebuilding your Jitsi installation

If you ever run into any trouble or if you have changed configuration (`jitsi_*` variables) too much, you can rebuild your Jitsi installation.

We normally don't recommend manual intervention, but Jitsi services tend to generate a lot of configuration files, and it is often wise to start afresh setting the services up, rather than messing with the existing configuration files. Since not all of those files are managed by Ansible (at least not yet), you may sometimes need to delete them by yourself manually.

To rebuild your Jitsi configuration, follow the procedure below:

- run this command locally to stop all Jitsi services: `just run-tags stop-group --extra-vars=group=jitsi`
- log in the server with SSH
- run this command remotely to remove all Jitsi configuration & data: `rm -rf /matrix/jitsi`
- run this command locally to set up Jitsi anew and restart services: `just install-service jitsi`
