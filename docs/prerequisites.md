# Prerequisites

- An x86 server running **CentOS** (7 only for now; [8 is not yet supported](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/300)), **Debian** (9/Stretch+), **Ubuntu** (16.04+), or **Archlinux**. This playbook doesn't support running on ARM ([see](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/299)), however a minimal subset of the tools can be built on the host, which may result in a working configuration, even on a Raspberry pi (see [Alternative Architectures](alternative-architectures.md)). We only strive to support released stable versions of distributions, not betas or pre-releases. This playbook can take over your whole server or co-exist with other services that you have there.

- `root` access to your server (or a user capable of elevating to `root` via `sudo`).

- [Python](https://www.python.org/) being installed on the server. Most distributions install Python by default, but some don't (e.g. Ubuntu 18.04) and require manual installation (something like `apt-get install python`).

- a `cron`-like tool installed on the server such as `cron` or `anacron` to automatically schedule the Let's Encrypt SSL certificates's renewal. *This can be ignored if you use your own SSL certificates.*

- the [Ansible](http://ansible.com/) program being installed on your own computer. It's used to run this playbook and configures your server for you. Take a look at [our guide about Ansible](ansible.md) for more information, as well as [version requirements](ansible.md#supported-ansible-versions) and alternative ways to run Ansible.

- either the `dig` tool or `python-dns` installed on your own computer. Used later on, by the playbook's [services check](maintenance-checking-services.md) feature.

- an HTTPS-capable web server at the base domain name (`<your-domain>`) which is capable of serving static files. Unless you decide to [Serve the base domain from the Matrix server](configuring-playbook-base-domain-serving.md) or alternatively, to use DNS SRV records for [Server Delegation](howto-server-delegation.md).

- properly configured DNS records for `<your-domain>` (details in [Configuring DNS](configuring-dns.md))

- some TCP/UDP ports open. This playbook configures the server's internal firewall for you. In most cases, you don't need to do anything special. But **if your server is running behind another firewall**, you'd need to open these ports: `80/tcp` (HTTP webserver), `443/tcp` (HTTPS webserver), `3478/tcp` (TURN over TCP), `3478/udp` (TURN over UDP), `5349/tcp` (TURN over TCP), `5349/udp` (TURN over UDP), `8448/tcp` (Matrix Federation API HTTPS webserver), the range `49152-49172/udp` (TURN over UDP), `4443/tcp` (Jitsi Harvester fallback), `10000/udp` (Jitsi video RTP)

When ready to proceed, continue with [Configuring DNS](configuring-dns.md).
