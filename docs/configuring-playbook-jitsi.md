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

Jitsi can not only be integrated with Element clients ([Element Web](configuring-playbook-client-element-web.md)/Desktop, Android and iOS) as a widget, but also be used as standalone web app.

The Ansible role for Jitsi is developed and maintained by [MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi). For details about configuring Jitsi, you can check them via:
- [the role's document at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md)
- `roles/galaxy/jitsi/docs/configuring-jitsi.md` locally, if you have fetched the Ansible roles

## Prerequisites

You may need to open the following ports to your server:

- `4443/tcp` — RTP media fallback over TCP
- `10000/udp` — RTP media over UDP. Depending on your firewall/NAT configuration, incoming RTP packets on port `10000` may have the external IP of your firewall as destination address, due to the usage of STUN in JVB (see [`jitsi_jvb_stun_servers`](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/defaults/main.yml)).

## Adjusting DNS records

By default, this playbook installs Jitsi on the `jitsi.` subdomain (`jitsi.example.com`) and requires you to create a CNAME record for `jitsi`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Jitsi, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
jitsi_enabled: true
```

### Adjusting the Jitsi URL (optional)

By tweaking the `jitsi_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname
jitsi_hostname: call.example.com
```

After changing the domain, **you may need to adjust your DNS** records to point the Jitsi domain to the Matrix server.

### Configure Jitsi authentication and guests mode (optional)

By default the Jitsi instance does not require for anyone to log in, and is open to use without an account. To control who is allowed to start meetings on your Jitsi instance, you'd need to enable Jitsi's authentication and optionally guests mode.

Authentication type must be one of them: `internal` (default), `jwt`, `matrix` or `ldap`. Currently, only `internal`, `matrix` and `ldap` mechanisms are supported by the [Jitsi role](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi).

With authentication enabled, all meetings have to be started by a registered user. After the meeting is started by that user, then guests are free to join. If the registered user is not yet present, the guests are put on hold in individual waiting rooms.

**Note**: authentication is not tested by the playbook's self-checks. We therefore recommend that you would make sure by yourself that authentication is configured properly. To test it, start a meeting at `jitsi.example.com` on your browser.

#### Authenticate using Jitsi accounts: Auth-Type `internal` (recommended)

The default authentication mechanism is `internal` auth, which requires a Jitsi account to have been configured. This is a recommended method, as it also works in federated rooms.

To enable authentication with a Jitsi account, add the following configuration to your `vars.yml` file. Make sure to replace `USERNAME_…` and `PASSWORD_…` with your own values.

```yaml
jitsi_enable_auth: true
jitsi_enable_guests: true
jitsi_prosody_auth_internal_accounts:
  - username: "USERNAME_FOR_THE_FIRST_USER_HERE"
    password: "PASSWORD_FOR_THE_FIRST_USER_HERE"
  - username: "USERNAME_FOR_THE_SECOND_USER_HERE"
    password: "PASSWORD_FOR_THE_SECOND_USER_HERE"
```

**Note**: as Jitsi account removal function is not integrated into the playbook, these accounts will not be able to be removed from the Prosody server automatically, even if they are removed from your `vars.yml` file subsequently.

#### Authenticate using Matrix OpenID: Auth-Type `matrix`

> [!WARNING]
> This breaks the Jitsi instance on federated rooms probably and does not allow sharing conference links with guests.

This authentication method requires [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service), which can be installed using this [playbook](configuring-playbook-user-verification-service.md). It verifies against Matrix openID, and requires a user-verification-service to run.

To enable authentication with Matrix OpenID, add the following configuration to your `vars.yml` file:

```yaml
jitsi_enable_auth: true
jitsi_auth_type: matrix
matrix_user_verification_service_enabled: true
```

For more information see also [https://github.com/matrix-org/prosody-mod-auth-matrix-user-verification](https://github.com/matrix-org/prosody-mod-auth-matrix-user-verification).

#### Authenticate using LDAP: Auth-Type `ldap`

To enable authentication with LDAP, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
jitsi_enable_auth: true
jitsi_auth_type: ldap
jitsi_ldap_url: "ldap://ldap.example.com"
jitsi_ldap_base: "OU=People,DC=example.com"
#jitsi_ldap_binddn: ""
#jitsi_ldap_bindpw: ""
jitsi_ldap_filter: "uid=%u"
jitsi_ldap_auth_method: "bind"
jitsi_ldap_version: "3"
jitsi_ldap_use_tls: true
jitsi_ldap_tls_ciphers: ""
jitsi_ldap_tls_check_peer: true
jitsi_ldap_tls_cacert_file: "/etc/ssl/certs/ca-certificates.crt"
jitsi_ldap_tls_cacert_dir: "/etc/ssl/certs"
jitsi_ldap_start_tls: false
```

For more information refer to the [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet#authentication-using-ldap) and the [saslauthd `LDAP_SASLAUTHD`](https://github.com/winlibs/cyrus-sasl/blob/master/saslauthd/LDAP_SASLAUTHD) documentation.

### Configure `JVB_ADVERTISE_IPS` for running behind NAT or on a LAN environment (optional)

When running Jitsi in a LAN environment, or on the public Internet via NAT, the `JVB_ADVERTISE_IPS` enviornment variable should be set.

This variable allows to control which IP addresses the JVB will advertise for WebRTC media traffic. It is necessary to set it regardless of the use of a reverse proxy, since it's the IP address that will receive the media (audio / video) and not HTTP traffic, hence it's oblivious to the reverse proxy.

If your users are coming in over the Internet (and not over LAN), this will likely be your public IP address. If this is not set up correctly, calls will crash when more than two users join a meeting.

To set the variable, add the following configuration to your `vars.yml` file. Make sure to replace `LOCAL_IP_ADDRESS_OF_THE_HOST_HERE` with a proper value.

```yaml
jitsi_jvb_container_extra_arguments:
  - '--env "JVB_ADVERTISE_IPS=LOCAL_IP_ADDRESS_OF_THE_HOST_HERE"'
```

Check [the official documentation](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/#running-behind-nat-or-on-a-lan-environment) for more details about it.

### Set a maximum number of participants on a Jitsi conference (optional)

You can set a maximum number of participants allowed to join a Jitsi conference. By default the number is not specified.

To set it, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
jitsi_prosody_max_participants: 4 # example value
```

### Enable Gravatar (optional)

In the default Jisti Meet configuration, `gravatar.com` is enabled as an avatar service.

Since the Element clients send the URL of configured Matrix avatars to the Jitsi instance, our default configuration has disabled the Gravatar service.

To enable the Gravatar service, add the following configuration to your `vars.yml` file:

```yaml
jitsi_disable_gravatar: false
```

> [!WARNING]
> This will result in third party request leaking data to the Gravatar Service (`gravatar.com`, unless configured otherwise). Besides metadata, the Matrix user_id and possibly the room ID (via `referrer` header) will be also sent to the third party.

### Fine tune Jitsi (optional)

If you'd like to have Jitsi save up resources, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
jitsi_web_config_resolution_width_ideal_and_max: 480
jitsi_web_config_resolution_height_ideal_and_max: 240
jitsi_web_custom_config_extension: |
  config.enableLayerSuspension = true;

  config.disableAudioLevels = true;

  config.channelLastN = 4;
```

These configurations:

- **limit the maximum video resolution**, to save up resources on both server and clients
- **suspend unused video layers** until they are requested again, to save up resources on both server and clients. Read more on this feature [here](https://jitsi.org/blog/new-off-stage-layer-suppression-feature/).
- **disable audio levels** to avoid excessive refresh of the client-side page and decrease the CPU consumption involved
- **limit the number of video feeds forwarded to each client**, to save up resources on both server and clients. As clients’ bandwidth and CPU may not bear the load, use this setting to avoid lag and crashes. This feature is available by default on other webconference applications such as Office 365 Teams (the number is limited to 4). Read how it works [here](https://github.com/jitsi/jitsi-videobridge/blob/5ff195985edf46c9399dcf263cb07167f0a2c724/doc/allocation.md).

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [Jitsi role](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using these variables:
  - `jitsi_web_custom_interface_config_extension`: custom configuration to be appended to `interface_config.js`, passed to Jitsi Web
  - `jitsi_web_custom_config_extension`: custom configuration to be injected into `custom-config.js`, passed to Jitsi Web
  - `jitsi_jvb_custom_config_extension`: custom configuration to be injected into `custom-sip-communicator.properties`, passed to Jitsi JVB

### Example configurations

Here is an example set of configurations for running a Jitsi instance with:

- authentication using a Jitsi account (username: `US3RNAME`, password: `passw0rd`)
- guests: allowed
- maximum participants: 6 people
- fine tuning with the configurations presented above
- other miscellaneous options (see the official Jitsi documentation [here](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-configuration) and [here](https://jitsi.github.io/handbook/docs/user-guide/user-guide-advanced))

```yaml
jitsi_enabled: true
jitsi_enable_auth: true
jitsi_enable_guests: true
jitsi_prosody_auth_internal_accounts:
  - username: "US3RNAME"
    password: "passw0rd"
jitsi_prosody_max_participants: 6
jitsi_web_config_resolution_width_ideal_and_max: 480
jitsi_web_config_resolution_height_ideal_and_max: 240
jitsi_web_custom_config_extension: |
  config.enableLayerSuspension = true;
  config.disableAudioLevels = true;
  config.channelLastN = 4;
  config.requireDisplayName = true; // force users to set a display name
  config.startAudioOnly = true; // start the conference in audio only mode (no video is being received nor sent)
```

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

- **directly (without any Matrix integration)**. Just go to `https://jitsi.example.com`

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
