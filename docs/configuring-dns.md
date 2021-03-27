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

## DNS settings for services enabled by default

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| A     | `matrix`                     | -        | -      | -    | `matrix-server-IP`     |
| CNAME | `element`                    | -        | -      | -    | `matrix.<your-domain>` |

Be mindful as to how long it will take for the DNS records to propagate.

If you are using Cloudflare DNS, make sure to disable the proxy and set all records to `DNS only`. Otherwise, fetching certificates will fail.

## DNS settings for optional services/features

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| SRV   | `_matrix-identity._tcp`      | 10       | 0      | 443  | `matrix.<your-domain>` |
| CNAME | `dimension` (*)              | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `jitsi` (*)                  | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `stats` (*)                  | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `goneb` (*)                  | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `sygnal` (*)                 | -        | -      | -    | `matrix.<your-domain>` |

## Subdomains setup

As the table above illustrates, you need to create 2 subdomains (`matrix.<your-domain>` and `element.<your-domain>`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` record is fine).

The `element.<your-domain>` subdomain may be necessary, because this playbook installs the [Element](https://github.com/vector-im/element-web) web client for you.
If you'd rather instruct the playbook not to install Element (`matrix_client_element_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `element.<your-domain>` DNS record.

The `dimension.<your-domain>` subdomain may be necessary, because this playbook could install the [Dimension integrations manager](http://dimension.t2bot.io/) for you. Dimension installation is disabled by default, because it's only possible to install it after the other Matrix services are working (see [Setting up Dimension](configuring-playbook-dimension.md) later). If you do not wish to set up Dimension, feel free to skip the `dimension.<your-domain>` DNS record.

The `jitsi.<your-domain>` subdomain may be necessary, because this playbook could install the [Jitsi video-conferencing platform](https://jitsi.org/) for you. Jitsi installation is disabled by default, because it may be heavy and is not a core required component. To learn how to install it, see our [Jitsi](configuring-playbook-jitsi.md) guide. If you do not wish to set up Jitsi, feel free to skip the `jitsi.<your-domain>` DNS record.

The `stats.<your-domain>` subdomain may be necessary, because this playbook could install [Grafana](https://grafana.com/) and setup performance metrics for you. Grafana installation is disabled by default, it is not a core required component. To learn how to install it, see our [metrics and graphs guide](configuring-playbook-prometheus-grafana.md). If you do not wish to set up Grafana, feel free to skip the `stats.<your-domain>` DNS record. It is possible to install Prometheus without installing Grafana, this would also not require the `stats.<your-domain>` subdomain.

The `goneb.<your-domain>` subdomain may be necessary, because this playbook could install the [Go-NEB](https://github.com/matrix-org/go-neb) bot. The installation of Go-NEB is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Go-NEB guide](configuring-playbook-bot-go-neb.md). If you do not wish to set up Go-NEB, feel free to skip the `goneb.<your-domain>` DNS record.

The `sygnal.<your-domain>` subdomain may be necessary, because this playbook could install the [Sygnal](https://github.com/matrix-org/sygnal) push gateway. The installation of Sygnal is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Sygnal guide](configuring-playbook-sygnal.md). If you do not wish to set up Sygnal (you probably don't, unless you're also developing/building your own Matrix apps), feel free to skip the `sygnal.<your-domain>` DNS record.


## `_matrix-identity._tcp` SRV record setup

To make the [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server (which this playbook installs for you) enable its federation features, set up an SRV record that looks like this:
- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.<your-domain>` (replace `<your-domain>` with your own)

This is an optional feature. See [ma1sd's documentation](https://github.com/ma1uta/ma1sd/wiki/mxisd-and-your-privacy#choices-are-never-easy) for information on the privacy implications of setting up this SRV record.

Note: This `_matrix-identity._tcp` SRV record for the identity server is different from the `_matrix._tcp` that can be used for Synapse delegation. See [howto-server-delegation.md](howto-server-delegation.md) for more information about delegation.

When you're done with the DNS configuration and ready to proceed, continue with [Configuring this Ansible playbook](configuring-playbook.md).
