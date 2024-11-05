# Prerequisites

<sup>⚡️[Quick start](README.md) | Prerequisites > [Configuring your DNS server](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md) </sup>

To install Matrix services using this Ansible playbook, you need:

- (Recommended) An **x86** server ([What kind of server specs do I need?](faq.md#what-kind-of-server-specs-do-i-need)) running one of these operating systems that make use of [systemd](https://systemd.io/):
  - **Archlinux**
  - **CentOS**, **Rocky Linux**, **AlmaLinux**, or possibly other RHEL alternatives (although your mileage may vary)
  - **Debian** (10/Buster or newer)
  - **Ubuntu** (18.04 or newer, although [20.04 may be problematic](ansible.md#supported-ansible-versions) if you run the Ansible playbook on it)

  Generally, newer is better. We only strive to support released stable versions of distributions, not betas or pre-releases. This playbook can take over your whole server or co-exist with other services that you have there.

  This playbook somewhat supports running on non-`amd64` architectures like ARM. See [Alternative Architectures](alternative-architectures.md).

  If your distro runs within an [LXC container](https://linuxcontainers.org/), you may hit [this issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/703). It can be worked around, if absolutely necessary, but we suggest that you avoid running from within an LXC container.

- `root` access to your server (or a user capable of elevating to `root` via `sudo`).

- [Python](https://www.python.org/) being installed on the server. Most distributions install Python by default, but some don't (e.g. Ubuntu 18.04) and require manual installation (something like `apt-get install python3`). On some distros, Ansible may incorrectly [detect the Python version](https://docs.ansible.com/ansible/latest/reference_appendices/interpreter_discovery.html) (2 vs 3) and you may need to explicitly specify the interpreter path in `inventory/hosts` during installation (e.g. `ansible_python_interpreter=/usr/bin/python3`)

- [sudo](https://www.sudo.ws/) being installed on the server, even when you've configured Ansible to log in as `root`. Some distributions, like a minimal Debian net install, do not include the `sudo` package by default.

- The [Ansible](http://ansible.com/) program being installed on your own computer. It's used to run this playbook and configures your server for you. Take a look at [our guide about Ansible](ansible.md) for more information, as well as [version requirements](ansible.md#supported-ansible-versions) and alternative ways to run Ansible.

- the [passlib](https://passlib.readthedocs.io/en/stable/index.html) Python library installed on the computer you run Ansible. On most distros, you need to install some `python-passlib` or `py3-passlib` package, etc.

- [`git`](https://git-scm.com/) is the recommended way to download the playbook to your computer. `git` may also be required on the server if you will be [self-building](self-building.md) components.

- [`just`](https://github.com/casey/just) for running `just roles`, `just update`, etc. (see [`justfile`](../justfile)), although you can also run these commands manually

- An HTTPS-capable web server at the base domain name (`example.com`) which is capable of serving static files. Unless you decide to [Serve the base domain from the Matrix server](configuring-playbook-base-domain-serving.md) or alternatively, to use DNS SRV records for [Server Delegation](howto-server-delegation.md).

- Properly configured DNS records for `example.com` (details in [Configuring DNS](configuring-dns.md)).

- Some TCP/UDP ports open. This playbook (actually [Docker itself](https://docs.docker.com/network/iptables/)) configures the server's internal firewall for you. In most cases, you don't need to do anything special. But **if your server is running behind another firewall**, you'd need to open these ports:

  - `80/tcp`: HTTP webserver
  - `443/tcp` and `443/udp`: HTTPS webserver
  - `3478/tcp`: TURN over TCP (used by Coturn)
  - `3478/udp`: TURN over UDP (used by Coturn)
  - `5349/tcp`: TURN over TCP (used by Coturn)
  - `5349/udp`: TURN over UDP (used by Coturn)
  - `8448/tcp` and `8448/udp`: Matrix Federation API HTTPS webserver. In some cases, this **may necessary even with federation disabled**. Integration Servers (like Dimension) and Identity Servers (like ma1sd) may need to access `openid` APIs on the federation port.
  - the range `49152-49172/udp`: TURN over UDP
  - potentially some other ports, depending on the additional (non-default) services that you enable in the **configuring the playbook** step (later on). Consult each service's documentation page in `docs/` for that.

When ready to proceed, continue with [Configuring DNS](configuring-dns.md).
