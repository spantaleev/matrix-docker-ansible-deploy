# Configuring your DNS server

To set up Matrix on your domain, you'd need to do some DNS configuration.

To use an identifier like `@<username>:<your-domain>`, you don't actually need
to install anything on the actual `<your-domain>` server.

You do, however need to instruct the Matrix network that Matrix services for `<your-domain>` are delegated
over to `matrix.<your-domain>`.
As we discuss in [Server Delegation](howto-server-delegation.md), there are 2 different ways to set up such delegation:

- either by serving a `https://<your-domain>/.well-known/matrix/server` file (from the base domain!)
- or by  using a `_matrix._tcp` DNS SRV record (don't confuse this with the `_matrix-identity._tcp` SRV record described below)

This playbook mostly discusses the well-known file method, because it's easier to manage with regard to certificates.
If you decide to go with the alternative method ([Server Delegation via a DNS SRV record (advanced)](howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced)), please be aware that the general flow that this playbook guides you through may not match what you need to do.


## General outline of DNS settings you need to do

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| A     | `matrix`                     | -        | -      | -    | `matrix-server-IP`     |
| CNAME | `element`                    | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `dimension` (*)              | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `jitsi` (*)                  | -        | -      | -    | `matrix.<your-domain>` |
| SRV   | `_matrix-identity._tcp`      | 10       | 0      | 443  | `matrix.<your-domain>` |


DNS records marked with `(*)` above are optional. They refer to services that will not be installed by default (see the section below). If you won't be installing these services, feel free to skip creating these DNS records. Also be mindful as to how long it will take for the DNS records to propagate.


## Subdomains setup

As the table above illustrates, you need to create 2 subdomains (`matrix.<your-domain>` and `element.<your-domain>`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` record is fine).

The `element.<your-domain>` subdomain is necessary, because this playbook installs the [Element](https://github.com/vector-im/element-web) web client for you.
If you'd rather instruct the playbook not to install Element (`matrix_client_element_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `element.<your-domain>` DNS record.

The `dimension.<your-domain>` subdomain may be necessary, because this playbook could install the [Dimension integrations manager](http://dimension.t2bot.io/) for you. Dimension installation is disabled by default, because it's only possible to install it after the other Matrix services are working (see [Setting up Dimension](configuring-playbook-dimension.md) later). If you do not wish to set up Dimension, feel free to skip the `dimension.<your-domain>` DNS record.

The `jitsi.<your-domain>` subdomain may be necessary, because this playbook could install the [Jitsi video-conferencing platform](https://jitsi.org/) for you. Jitsi installation is disabled by default, because it may be heavy and is not a core required component. To learn how to install it, see our [Jitsi](configuring-playbook-jitsi.md) guide. If you do not wish to set up Jitsi, feel free to skip the `jitsi.<your-domain>` DNS record.


## `_matrix-identity._tcp` SRV record setup

To make the [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server (which this playbook installs for you) be authoritative for your domain name, set up one more SRV record that looks like this:
- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.<your-domain>` (replace `<your-domain>` with your own)


When you're done with the DNS configuration and ready to proceed, continue with [Configuring this Ansible playbook](configuring-playbook.md).
