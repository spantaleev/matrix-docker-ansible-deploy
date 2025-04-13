<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->
# Configuring IPv6

Since 2025-03-08, the [default example configuration](../examples/vars.yml) for the playbook recommends enabling [IPv6](https://en.wikipedia.org/wiki/IPv6) support for Docker's container networks.

**If you have IPv6 support on your server/network** (see [How do I check if my server has IPv6 connectivity?](#how-do-i-check-if-my-server-has-ipv6-connectivity)), then [enabling IPv6 support for the playbook](#enabling-ipv6-support-for-the-playbook) would give you:

- 📥 incoming IPv6 connectivity to the server via the server's IPv6 address/addresses (containers won't have their own individual publicly accessible IPs)
- 📤 outgoing IPv6 connectivity from the server via the server's IPv6 address/addresses (containers won't exit via their own individual IPv6 address)
- 🔄 IPv6 connectivity for cross-container communication

**If you still don't have IPv6 support on your server/network**, then enabling IPv6 support for the playbook will only enable IPv6 connectivity for cross-container communication and shouldn't affect your server's incoming/outgoing communication. You may also be interested in reading if [there's a performance penalty to enabling IPv6 if the server/network doesn't support IPv6 connectivity?](#is-there-a-performance-penalty-to-enabling-ipv6-if-the-server-network-doesn-t-support-ipv6-connectivity)

As such, **we recommend that you follow the default example configuration and leave IPv6 support for Docker enabled in all cases**.

Enabling IPv6 consists of 2 steps:

- [Enabling IPv6 support for the playbook](#enabling-ipv6-support-for-the-playbook)
- [Configuring DNS records for IPv6](#configuring-dns-records-for-ipv6)

💡 If you've followed a recent version of our documentation, you would have already done these steps, so there's nothing else to do.

## Enabling IPv6 support for the playbook

You can enable IPv6 support for all components' Docker container networks by using the following `vars.yml` configuration:

```yml
# Controls whether container networks will be created with IPv6 support.
#
# If you also have IPv6 support on your server/network and AAAA DNS records pointing to the server,
# enabling this will effectively give you full public IPv6 connectivity (powered by NAT66).
#
# We recommend leaving this enabled even if you don't currently have IPv6 connectivity on your server/network.
# This way, once you eventually get IPv6 connectivity, you won't have to change anything (besides DNS records).
#
# Flipping this setting later on requires manual work (stopping services, deleting and recreating all container networks).
#
# In the future, this setting will likely default to `true`, so if you really want IPv6 disabled, explicitly set this to `false`.
#
# People managing Docker themselves and running an older Docker version will need additional configuration.
#
# Learn more in `docs/configuring-ipv6.md`.
devture_systemd_docker_base_ipv6_enabled: true
```

Doing this:

- all container networks will be IPv6-enabled

- NAT66 will be used, so that:
  - containers will get [Unique Local Addresses (ULA)](https://en.wikipedia.org/wiki/Unique_local_address)
  - the outgoing IPv6 address for containers will be the same as the one on the server
  - traffic destined for the IPv6 address of the server will be forwarded to the containers that handle (and publish) that specific port

> [!WARNING]
> Without enabling this and assuming you have IPv6 `AAAA` DNS records pointing to the server (see [Configuring DNS records for IPv6](#configuring-dns-records-for-ipv6)), IPv6 traffic will still be handled, but NAT64 will be used instead of NAT66.
> As such, containers will only have an IPv4 address and all IPv6 traffic that reaches them will seem to originate from a local IP. Containers also won't be able to make outgoing (even cross-container) IPv6 requests.

To confirm connectivity, see the following other resources:

- [How do I check if my server has IPv6 connectivity?](#how-do-i-check-if-my-server-has-ipv6-connectivity)
- [How do I check outgoing IPv6 connectivity for containers?](#how-do-i-check-outgoing-ipv6-connectivity-for-containers)
- [How do I check incoming IPv6 connectivity for containers?](#how-do-i-check-incoming-ipv6-connectivity-for-containers)
- [How do I confirm if my container networks are IPv6-enabled?](#how-do-i-confirm-if-my-container-networks-are-ipv6-enabled)
- Ensure that the [Federation Tester](https://federationtester.matrix.org/) reports that your server is reachable over IPv6.

## Configuring DNS records for IPv6

[Enabling IPv6 support for the playbook](#enabling-ipv6-support-for-the-playbook) tells you how to prepare for IPv6 on the container (Docker) side.

For full public IPv6 connectivity (and not just IPv6 connectivity for containers inside the container networks) you also need to **ensure that your domain names** (e.g. `matrix.example.com` and others) have IPv6 (`AAAA`) DNS records pointing to the server's IPv6 address.

Also see the [Configuring DNS settings](configuring-dns.md) documentation page for more details.

### A note about old Docker

With our [default example configuration](../examples/vars.yml), the playbook manages Docker for you and installs a modern-enough version.

Docker versions newer than 27.0.1 enable IPv6 integration at the Docker daemon level out of the box. This still requires that networks are created with IPv6 support as described in the [Enabling IPv6 support for the playbook](#enabling-ipv6-support-for-the-playbook) section above.

**If you're on an old Docker version** (Docker 27.0.0 or older) for some reason, it's likely that your Docker installation is not enabled for IPv6 at all. In such a case:

- if Docker is managed by the playbook, you can tell it to force-enable IPv6 via `devture_systemd_docker_base_ipv6_daemon_options_changing_enabled: true`

- if Docker is managed by you manually, you can add `{"experimental": true, "ip6tables": true}` to the Docker daemon options and restart the Docker service (`docker.service`).

### Frequently Asked Questions

#### How do I check if my server has IPv6 connectivity?

##### With curl

You can run `curl https://icanhazip.com` and see if it returns an [IPv6 address](https://en.wikipedia.org/wiki/IPv6_address) (an address with `:` characters in it, like `2001:db8:1234:5678::1`). If it does, then your server has IPv6 connectivity and prefers it over using IPv4. This is common.

If you see an IPv4 address instead (e.g. `1.2.3.4`), it may be that your server prefers IPv4 over IPv6 or that your network does not support IPv6. You can try forcing `curl` to use IPv6 by running `curl -6 https://icanhazip.com` and see if it returns an IPv6 address.

##### With other network utilities

You can run `ip -6 addr` to see if you have any IPv6 addresses assigned to your server, besides the link-local (`fe80::*`) addresses that everyone has (unless they have force-disabled IPv6 support on their system).

If you do have an IPv6 address, it's still worth [using curl](#with-curl) to confirm that your server can successfully make outgoing requests over IPv6.

#### What does the `devture_systemd_docker_base_ipv6_enabled` setting actually do?

The `devture_systemd_docker_base_ipv6_enabled` setting controls whether container networks will be created with IPv6 support.

Changing this setting subsequently requires manual work (deleting all container networks).
See [I've changed the `devture_systemd_docker_base_ipv6_enabled` setting, but it doesn't seem to have any effect](#i-ve-changed-the-devture_systemd_docker_base_ipv6_enabled-setting-but-it-doesn-t-seem-to-have-any-effect).

#### I've changed the `devture_systemd_docker_base_ipv6_enabled` setting, but it doesn't seem to have any effect.

If you're using an older Docker version (Docker 27.0.0 or older), see [A note about old Docker](#a-note-about-old-docker).

If you've previously installed with one `devture_systemd_docker_base_ipv6_enabled` value and then changed it to another, you need to:

- stop all services (`just stop-all`)
- delete all container networks on the server: `docker network rm $(docker network ls -q)`
- re-run the playbook fully: `just install-all`

#### How do I confirm if my container networks are IPv6-enabled?

You can list container networks by running `docker network ls` on the server.

For each container network (e.g. `matrix-homeserver`), you can check if it has IPv6 connectivity by running a command like this: `docker network inspect matrix-homeserver`.

Ensure that there's an IPv6 subnet/gateway in the `IPAM.Config` section. If yes, you may wish to proceed with [How do I check outgoing IPv6 connectivity for containers?](#how-do-i-check-outgoing-ipv6-connectivity-for-containers)

If there's no IPv6 subnet/gateway in the `IPAM.Config` section, this container network was not created with IPv6 support.
See [I've changed the `devture_systemd_docker_base_ipv6_enabled` setting, but it doesn't seem to have any effect](#i-ve-changed-the-devture_systemd_docker_base_ipv6_enabled-setting-but-it-doesn-t-seem-to-have-any-effect).

#### How do I check outgoing IPv6 connectivity for containers?

```sh
docker run --rm --network=matrix-homeserver quay.io/curl/curl:latest curl -6 https://icanhazip.com
```

💡 This one-off container is connected to the `matrix-homeserver` container network, not to the default Docker bridge network. The default Docker `bridge` network does not have IPv6 connectivity by default (yet) and is not influenced by the `devture_systemd_docker_base_ipv6_enabled` setting, so using that network (by omitting `--network=..` from the command above) will not show an IPv6 address

✅ If this command returns an IPv6 address, you're all good.

❌ If this command doesn't return an IPv6 address, it may be that:

- your container network does not have IPv6 connectivity. See [How do I confirm if my container networks are IPv6-enabled?](#how-do-i-confirm-if-my-container-networks-are-ipv6-enabled) for more details.

- your server does not have IPv6 connectivity. See [How do I check if my server has IPv6 connectivity?](#how-do-i-check-if-my-server-has-ipv6-connectivity) for more details. If you do have IPv6 connectivity, then the issue is with Docker's IPv6 configuration. Otherwise, you need to check your server's network configuration/firewall/routing and get back to configuring the playbook later on.

#### How do I check incoming IPv6 connectivity for containers?

Only containers that publish ports will be exposed (reachable) publicly on the server's own IPv6 address. Containers will not get their own individual public IPv6 address.

For this playbook, a commonly exposed container is the Traefik reverse-proxy container (unless [you're using your own webserver](./configuring-playbook-own-webserver.md)).

You can either do something like `curl -6 https://matrix.example.com` from an IPv6-enabled host (including the server itself) and see if it works.

An alternative is to use the [IPv6 Port Checker](https://port.tools/port-checker-ipv6/) with a hostname of `matrix.example.com` and a port of `443`.

💡 Trying to connect to `matrix.example.com` via IPv6 requires that you have already [configured the DNS records for IPv6](#configuring-dns-records-for-ipv6) as described above. If you wish to eliminate DNS as a potential issue, you can also try connecting to the server's own IPv6 address directly: `curl -6 -H 'Host: matrix.example.com' https://[2001:db8:1234:5678::1]` (we pass a `Host` header to tell Traefik which host we'd like it to serve).

#### Why enable IPv6 if my network doesn't support it yet?

Because when your network does get support for IPv6 later on (even if that's 5 years away), you won't have to change anything besides [configuring the DNS records for IPv6](#configuring-dns-records-for-ipv6).

#### Can I use a custom subnet for IPv6?

Not easily.

The playbook and the various roles only support passing an `enable_ipv6` flag (`true` or `false` value depending on the `devture_systemd_docker_base_ipv6_enabled` Ansible variable) when creating the Docker container networks.

There's no support for passing a custom subnet for IPv4 and IPv6. We let Docker auto-generate the subnets for us.

You can either create a Pull Request that adds support for this to the various playbook roles, or you can manually recreate the networks from the command-line (e.g. `docker network rm matrix-homeserver && docker network create --ipv6 --subnet=2001:db8:1234:5678::/64 matrix-homeserver`).

#### Can I use Global Unicast Addresses (GUA) for IPv6?

No. You cannot have GUA addresses where each container is individually addressable over the public internet.

The playbook only supports NAT66, which should be good enough for most use cases.

Having containers get IPv6 addresses from your own GUA subnet requires complex configuration (ndp-proxy, etc.) and is not supported.

You may find [this Reddit post](https://www.reddit.com/r/ipv6/comments/1alpzmb/comment/kphpw11/) interesting.

#### Is there a performance penalty to enabling IPv6 if the server/network doesn't support IPv6 connectivity?

Probably a tiny one, as services may try to make (unsuccessful) outgoing requests over IPv6.

In practice, it's probably negligible.
