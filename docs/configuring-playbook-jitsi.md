# Jitsi

The playbook can install the [Jitsi](https://jitsi.org/) video-conferencing platform and integrate it with [Element](configuring-playbook-client-element.md).

Jitsi installation is **not enabled by default**, because it's not a core component of Matrix services.

The setup done by the playbook is very similar to [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet). You can refer to the documentation there for many of the options here.


## Prerequisites

Before installing Jitsi, make sure you've created the `jitsi.DOMAIN` DNS record (unless you've changed `jitsi_hostname`, as described below). See [Configuring DNS](configuring-dns.md) for details about DNS changes.

You may also need to open the following ports to your server:

- `4443/tcp` - RTP media fallback over TCP
- `10000/udp` - RTP media over UDP. Depending on your firewall/NAT setup, incoming RTP packets on port `10000` may have the external IP of your firewall as destination address, due to the usage of STUN in JVB (see [`jitsi_jvb_stun_servers`](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/defaults/main.yml)).


## Installation

Add this to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
jitsi_enabled: true

# Uncomment and adjust if you need to use another hostname
# jitsi_hostname: "jitsi.{{ matrix_domain }}"

# Uncomment and possible adjust if you'd like to host under a subpath
# jitsi_path_prefix: /jitsi
```

## (Optional) Configure Jitsi authentication and guests mode

By default the Jitsi Meet instance does not require any kind of login and is open to use for anyone without registration.

If you're fine with such an open Jitsi instance, please skip to [Apply changes](#apply-changes).

If you would like to control who is allowed to open meetings on your new Jitsi instance, then please follow the following steps to enable Jitsi's authentication and optionally guests mode.
Currently, there are three supported authentication modes: 'internal' (default), 'matrix' and 'ldap'.

**Note:** Authentication is not tested via the playbook's self-checks.
We therefore recommend that you manually verify if authentication is required by jitsi.
For this, try to manually create a conference on jitsi.DOMAIN in your browser.

### Authenticate using Jitsi accounts (Auth-Type 'internal')
The default authentication mechanism is 'internal' auth, which requires jitsi-accounts to be setup and is the recommended setup, as it also works in federated rooms.
With authentication enabled, all meeting rooms have to be opened by a registered user, after which guests are free to join.
If a registered host is not yet present, guests are put on hold in individual waiting rooms.

Add these lines to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
jitsi_enable_auth: true
jitsi_enable_guests: true
jitsi_prosody_auth_internal_accounts:
  - username: "jitsi-moderator"
    password: "secret-password"
  - username: "another-user"
    password: "another-password"
```

**Caution:** Accounts added here and subsequently removed will not be automatically removed from the Prosody server until user account cleaning is integrated into the playbook.

**If you get an error** like this: "Error: Account creation/modification not supported.", it's likely that you had previously installed Jitsi without auth/guest support. In such a case, you should look into [Rebuilding your Jitsi installation](#rebuilding-your-jitsi-installation).

### Authenticate using Matrix OpenID (Auth-Type 'matrix')

**Attention: Probably breaks Jitsi in federated rooms and does not allow sharing conference links with guests.**

Using this authentication type require a [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service).
By default, this playbook creates and configures a user-verification-service to run locally, see [configuring-user-verification-service](configuring-playbook-user-verification-service.md).

To enable set this configuration at host level:

```yaml
jitsi_enable_auth: true
jitsi_auth_type: matrix
matrix_user_verification_service_enabled: true
```

For more information see also [https://github.com/matrix-org/prosody-mod-auth-matrix-user-verification](https://github.com/matrix-org/prosody-mod-auth-matrix-user-verification).

### Authenticate using LDAP (Auth-Type 'ldap')

An example LDAP configuration could be:

```yaml
jitsi_enable_auth: true
jitsi_auth_type: ldap
jitsi_ldap_url: "ldap://ldap.DOMAIN"
jitsi_ldap_base: "OU=People,DC=DOMAIN"
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


## (Optional) Making your Jitsi server work on a LAN

By default the Jitsi Meet instance does not work with a client in LAN (Local Area Network), even if others are connected from WAN. There are no video and audio. In the case of WAN to WAN everything is ok.

The reason is the Jitsi VideoBridge git to LAN client the IP address of the docker image instead of the host. The [documentation](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/#running-behind-nat-or-on-a-lan-environment) of Jitsi in docker suggest to add `JVB_ADVERTISE_IPS` in enviornment variable to make it work.

Here is how to do it in the playbook.

Add these two lines to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
jitsi_jvb_container_extra_arguments:
  - '--env "JVB_ADVERTISE_IPS=<Local IP address of the host>"'
```

## (Optional) Fine tune Jitsi

Sample **additional** `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration to save up resources (explained below):

```yaml
jitsi_web_custom_config_extension: |
  config.enableLayerSuspension = true;

  config.disableAudioLevels = true;

  // Limit the number of video feeds forwarded to each client
  config.channelLastN = 4;

jitsi_web_config_resolution_width_ideal_and_max: 480
jitsi_web_config_resolution_height_ideal_and_max: 240
```

You may want to **suspend unused video layers** until they are requested again, to save up resources on both server and clients.
Read more on this feature [here](https://jitsi.org/blog/new-off-stage-layer-suppression-feature/)

You may wish to **disable audio levels** to avoid excessive refresh of the client-side page and decrease the CPU consumption involved.

You may want to **limit the number of video feeds forwarded to each client**, to save up resources on both server and clients. As clients’ bandwidth and CPU may not bear the load, use this setting to avoid lag and crashes.
This feature is found by default in other webconference applications such as Office 365 Teams (limit is set to 4).
Read how it works [here](https://github.com/jitsi/jitsi-videobridge/blob/master/doc/last-n.md) and performance evaluation on this [study](https://jitsi.org/wp-content/uploads/2016/12/nossdav2015lastn.pdf).

You may want to **limit the maximum video resolution**, to save up resources on both server and clients.

## (Optional) Specify a Max number of participants on a Jitsi conference

The playbook allows a user to set a max number of participants allowed to join a Jitsi conference. By default there is no limit.

In order to set the max number of participants use the following **additional** configuration:

```yaml
jitsi_prosody_max_participants: 4 # example value
```

## (Optional) Additional JVBs

By default, a single JVB ([Jitsi VideoBridge](https://github.com/jitsi/jitsi-videobridge)) is deployed on the same host as the Matrix server. To allow more video-conferences to happen at the same time, you may need to provision additional JVB services on other hosts.

There is an ansible playbook that can be run with the following tag:
`ansible-playbook -i inventory/hosts --limit jitsi_jvb_servers jitsi_jvb.yml --tags=common,setup-additional-jitsi-jvb,start`

For this role to work you will need an additional section in the ansible hosts file with the details of the JVB hosts, for example:
```
[jitsi_jvb_servers]
<your jvb hosts> ansible_host=<ip address of the jvb host>
```

Each JVB will require a server id to be set so that it can be uniquely identified and this allows Jitsi to keep track of which conferences are on which JVB.
The server id is set with the variable `jitsi_jvb_server_id` which ends up as the JVB_WS_SERVER_ID environment variables in the JVB docker container.
This variable can be set via the host file, a parameter to the ansible command or in the `vars.yaml` for the host which will have the additional JVB. For example:

``` yaml
jitsi_jvb_server_id: 'jvb-2'
```

``` INI
[jitsi_jvb_servers]
jvb-2.example.com ansible_host=192.168.0.2 jitsi_jvb_server_id=jvb-2
jvb-3.example.com ansible_host=192.168.0.3 jitsi_jvb_server_id=jvb-2
```

Note that the server id `jvb-1` is reserved for the JVB instance running on the Matrix host and therefore should not be used as the id of an additional jvb host.

The additional JVB will also need to expose the colibri web socket port and this can be done with the following variable:

```yaml
jitsi_jvb_container_colibri_ws_host_bind_port: 9090
```

The JVB will also need to know where the prosody xmpp server is located, similar to the server id this can be set in the vars for the JVB by using the variable
`jitsi_xmpp_server`. The Jitsi prosody container is deployed on the matrix server by default so the value can be set to the matrix domain. For example:

```yaml
jitsi_xmpp_server: "{{ matrix_domain }}"
```

However, it can also be set the ip address of the matrix server. This can be useful if you wish to use a private ip. For example:

```yaml
jitsi_xmpp_server: "192.168.0.1"
```

For the JVB to be able to contact the XMPP server, the latter must expose the XMPP port (5222). By default, the Matrix server does not expose the
port; only the XMPP container exposes it internally inside the host, which means that the first JVB (which runs on the Matrix server) can reach it but
the additional JVB cannot. The port is exposed by setting `jitsi_prosody_container_jvb_host_bind_port` like this:

```yaml
jitsi_prosody_container_jvb_host_bind_port: 5222
```

(The default is empty; if it's set then docker forwards the port.)

Applied together this will allow you to provision extra JVB instances which will register themselves with the prosody service and be available for jicofo
to route conferences too.

To make Traefik reverse-proxy to these additional JVBs (living on other hosts), **you would need to add the following Traefik configuration extension**:

```yaml
# Traefik proxying for additional JVBs. These can't be configured using Docker
# labels, like the first JVB is, because they run on different hosts, so we add
# the necessary configuration to the file provider.
devture_traefik_provider_configuration_extension_yaml: |
  http:
   routers:
     {% for host in groups['jitsi_jvb_servers'] %}

     additional-{{ hostvars[host]['jitsi_jvb_server_id'] }}-router:
       entryPoints:
         - "{{ devture_traefik_entrypoint_primary }}"
       rule: "Host(`{{ jitsi_hostname }}`) && PathPrefix(`/colibri-ws/{{ hostvars[host]['jitsi_jvb_server_id'] }}/`)"
       service: additional-{{ hostvars[host]['jitsi_jvb_server_id'] }}-service
       {% if devture_traefik_entrypoint_primary != 'web' %}

       tls:
         certResolver: "{{ devture_traefik_certResolver_primary }}"

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

## (Optional) Enable Gravatar

In the default Jisti Meet configuration, gravatar.com is enabled as an avatar service. This results in third party request leaking data to gravatar.
Since element already sends the url of configured Matrix avatars to Jitsi, we disabled gravatar.

To enable Gravatar set:

```yaml
jitsi_disable_gravatar: false
```

**Beware:** This leaks information to a third party, namely the Gravatar-Service (unless configured otherwise: gravatar.com).
Besides metadata, this includes the matrix user_id and possibly the room identifier (via `referrer` header).

## Apply changes

Then re-run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`


## Usage

You can use the self-hosted Jitsi server in multiple ways:

- **by adding a widget to a room via Element** (the one configured by the playbook at `https://element.DOMAIN`). Just start a voice or a video call in a room containing more than 2 members and that would create a Jitsi widget which utilizes your self-hosted Jitsi server.

- **by adding a widget to a room via the Dimension Integration Manager**. You'll have to point the widget to your own Jitsi server manually. See our [Dimension](./configuring-playbook-dimension.md) documentation page for more details. Naturally, Dimension would need to be installed first (the playbook doesn't install it by default).

- **directly (without any Matrix integration)**. Just go to `https://jitsi.DOMAIN`

**Note**: Element apps on mobile devices currently [don't support joining meetings on a self-hosted Jitsi server](https://github.com/element-hq/riot-web/blob/601816862f7d84ac47547891bd53effa73d32957/docs/jitsi.md#mobile-app-support).


## Troubleshooting

### Rebuilding your Jitsi installation

**If you ever run into any trouble** or **if you change configuration (`jitsi_*` variables) too much**, we urge you to rebuild your Jitsi setup.

We normally don't require such manual intervention for other services, but Jitsi services generate a lot of configuration files on their own.

These files are not all managed by Ansible (at least not yet), so you may sometimes need to delete them all and start fresh.

To rebuild your Jitsi configuration:

- ask Ansible to stop all Jitsi services: `just run-tags stop-group --extra-vars=group=jitsi`
- SSH into the server and do this and remove all Jitsi configuration & data (`rm -rf /matrix/jitsi`)
- ask Ansible to set up Jitsi anew and restart services (`just install-service jitsi`)
