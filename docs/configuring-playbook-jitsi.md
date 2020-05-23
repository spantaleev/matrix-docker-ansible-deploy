# Jitsi

The playbook can install the [Jitsi](https://jitsi.org/) video-conferencing platform and integrate it with [Riot](configuring-playbook-riot-web.md).

Jitsi installation is **not enabled by default**, because it's not a core component of Matrix services.

The setup done by the playbook is very similar to [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet). You can refer to the documentation there for many of the options here.


## Prerequisites

Before installing Jitsi, make sure you've created the `jitsi.DOMAIN` DNS record. See [Configuring DNS](configuring-dns.md).

You may also need to open the following ports to your server:

- `10000/udp` - RTP media over UDP
- `4443/tcp` - RTP media fallback over TCP


## Installation

Add this to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
matrix_jitsi_enabled: true

# Run `bash inventory/scripts/jitsi-generate-passwords.sh` to generate these passwords,
# or define your own strong passwords manually.
matrix_jitsi_jicofo_component_secret: ""
matrix_jitsi_jicofo_auth_password: ""
matrix_jitsi_jvb_auth_password: ""
matrix_jitsi_jibri_recorder_password: ""
matrix_jitsi_jibri_xmpp_password: ""
```


## (Optional) Configure Jitsi authentication and guests mode

By default the Jitsi Meet instance does not require any kind of login and is open to use for anyone without registration.

If you're fine with such an open Jitsi instance, please skip to [Apply changes](#apply-changes).

If you would like to control who is allowed to open meetings on your new Jitsi instance, then please follow this step to enable Jitsi's authentication and guests mode. With authentication enabled, all meeting rooms have to be opened by a registered user, after which guests are free to join. If a registered host is not yet present, guests are put on hold in individual waiting rooms.

Add these two lines to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
matrix_jitsi_enable_auth: true
matrix_jitsi_enable_guests: true
```

### (Optional) LDAP authentication

The default authentication mode of Jitsi is `internal`, however LDAP is also supported. An example LDAP configuration could be:

```yaml
matrix_jitsi_enable_auth: true
matrix_jitsi_auth_type: ldap
matrix_jitsi_ldap_url: ldap://ldap.DOMAIN  # or ldaps:// if using tls
matrix_jitsi_ldap_base: "OU=People,DC=DOMAIN"
matrix_jitsi_ldap_filter: "(&(uid=%u)(employeeType=active))"
matrix_jitsi_ldap_use_tls: false
matrix_jitsi_ldap_start_tls: true
```

For more information refer to the [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet#authentication-using-ldap) and the [saslauthd `LDAP_SASLAUTHD`](https://github.com/winlibs/cyrus-sasl/blob/master/saslauthd/LDAP_SASLAUTHD) documentation.


## (Optional) Making your Jitsi server work on a LAN

By default the Jitsi Meet instance does not work with a client in LAN (Local Area Network), even if others are connected from WAN. There are no video and audio. In the case of WAN to WAN everything is ok.

The reason is the Jitsi VideoBridge git to LAN client the IP address of the docker image instead of the host. The [documentation](https://github.com/jitsi/docker-jitsi-meet#running-behind-nat-or-on-a-lan-environment) of Jitsi in docker suggest to add `DOCKER_HOST_ADDRESS` in enviornment variable to make it work.

Here is how to do it in the playbook.

Add these two lines to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
matrix_jitsi_jvb_container_extra_arguments:
  - '--env "DOCKER_HOST_ADDRESS=<Local IP adress of the host>"'
```

## Apply changes

Then re-run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

## Required if configuring Jitsi with internal authentication: register new users

Until this gets integrated into the playbook, we need to register new users / meeting hosts for Jitsi manually.
Please SSH into your matrix host machine and execute the following command targeting the `matrix-jitsi-prosody` container:

```bash
docker exec matrix-jitsi-prosody prosodyctl --config /config/prosody.cfg.lua register <USERNAME> matrix-jitsi-web <PASSWORD>
```

Run this command for each user you would like to create, replacing `<USERNAME>` and `<PASSWORD>` accordingly. After you've finished, please exit the host.

**If you get an error** like this: "Error: Account creation/modification not supported.", it's likely that you had previously installed Jitsi without auth/guest support. In such a case, you should look into [Rebuilding your Jitsi installation](#rebuilding-your-jitsi-installation).


## Usage

You can use the self-hosted Jitsi server in multiple ways:

- **by adding a widget to a room via riot-web** (the one configured by the playbook at `https://riot.DOMAIN`). Just start a voice or a video call in a room containing more than 2 members and that would create a Jitsi widget which utilizes your self-hosted Jitsi server.

- **by adding a widget to a room via the Dimension Integration Manager**. You'll have to point the widget to your own Jitsi server manually. See our [Dimension](./configuring-playbook-dimension.md) documentation page for more details. Naturally, Dimension would need to be installed first (the playbook doesn't install it by default).

- **directly (without any Matrix integration)**. Just go to `https://jitsi.DOMAIN`

**Note**: Riot apps on mobile devices currently [don't support joining meetings on a self-hosted Jitsi server](https://github.com/vector-im/riot-web/blob/601816862f7d84ac47547891bd53effa73d32957/docs/jitsi.md#mobile-app-support).


## Troubleshooting

### Rebuilding your Jitsi installation

**If you ever run into any trouble** or **if you change configuration (`matrix_jitsi_*` variables) too much**, we urge you to rebuild your Jitsi setup.

We normally don't require such manual intervention for other services, but Jitsi services generate a lot of configuration files on their own.

These files are not all managed by Ansible (at least not yet), so you may sometimes need to delete them all and start fresh.

To rebuild your Jitsi configuration:

- SSH into the server and do this:
  - stop all Jitsi services (`systemctl stop matrix-jitsi-*`).
  - remove all Jitsi configuration & data (`rm -rf /matrix/jitsi`)
- ask Ansible to set up Jitsi anew and restart services (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-jitsi,start`)
