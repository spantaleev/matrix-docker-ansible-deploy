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

When you're done configuring DNS, proceed to [Configuring the playbook](configuring-playbook.md).

## DNS settings for optional services/features

| Used by component                                                                                                       | Type  | Host                           | Priority | Weight | Port | Target                      |
| ----------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------ | -------- | ------ | ---- | --------------------------- |
| [ma1sd](configuring-playbook-ma1sd.md) identity server                                                                  | SRV   | `_matrix-identity._tcp`        | 10       | 0      | 443  | `matrix.<your-domain>`      |
| [Dimension](configuring-playbook-dimension.md) integration server                                                       | CNAME | `dimension`                    | -        | -      | -    | `matrix.<your-domain>`      |
| [Jitsi](configuring-playbook-jitsi.md) video-conferencing platform                                                      | CNAME | `jitsi`                        | -        | -      | -    | `matrix.<your-domain>`      |
| [Prometheus/Grafana](configuring-playbook-prometheus-grafana.md) monitoring system                                      | CNAME | `stats`                        | -        | -      | -    | `matrix.<your-domain>`      |
| [Go-NEB](configuring-playbook-bot-go-neb.md) bot                                                                        | CNAME | `goneb`                        | -        | -      | -    | `matrix.<your-domain>`      |
| [Sygnal](configuring-playbook-sygnal.md) push notification gateway                                                      | CNAME | `sygnal`                       | -        | -      | -    | `matrix.<your-domain>`      |
| [ntfy](configuring-playbook-ntfy.md) push notifications server                                                          | CNAME | `ntfy`                         | -        | -      | -    | `matrix.<your-domain>`      |
| [Etherpad](configuring-playbook-etherpad.md) collaborative text editor                                                  | CNAME | `etherpad`                     | -        | -      | -    | `matrix.<your-domain>`      |
| [Hydrogen](configuring-playbook-client-hydrogen.md) web client                                                          | CNAME | `hydrogen`                     | -        | -      | -    | `matrix.<your-domain>`      |
| [Cinny](configuring-playbook-client-cinny.md) web client                                                                | CNAME | `cinny`                        | -        | -      | -    | `matrix.<your-domain>`      |
| [Buscarron](configuring-playbook-bot-buscarron.md) helpdesk bot                                                         | CNAME | `buscarron`                    | -        | -      | -    | `matrix.<your-domain>`      |
| [Postmoogle](configuring-playbook-bot-postmoogle.md)/[Email2Matrix](configuring-playbook-email2matrix.md) email bridges | MX    | `matrix`                       | 10       | 0      | -    | `matrix.<your-domain>`      |
| [Postmoogle](configuring-playbook-bot-postmoogle.md) email bridge                                                       | TXT   | `matrix`                       | -        | -      | -    | `v=spf1 ip4:<your-ip> -all` |
| [Postmoogle](configuring-playbook-bot-postmoogle.md) email bridge                                                       | TXT   | `_dmarc.matrix`                | -        | -      | -    | `v=DMARC1; p=quarantine;`   |
| [Postmoogle](configuring-playbook-bot-postmoogle.md) email bridge                                                       | TXT   | `postmoogle._domainkey.matrix` | -        | -      | -    | get it from `!pm dkim`      |

When setting up a SRV record, if you are asked for a service and protocol instead of a hostname split the host value from the table where the period is. For example use service as `_matrix-identity` and protocol as `_tcp`.

## Subdomains setup

As the table above illustrates, you need to create 2 subdomains (`matrix.<your-domain>` and `element.<your-domain>`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` record is fine).

The `element.<your-domain>` subdomain may be necessary, because this playbook installs the [Element](https://github.com/vector-im/element-web) web client for you.
If you'd rather instruct the playbook not to install Element (`matrix_client_element_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `element.<your-domain>` DNS record.

The `dimension.<your-domain>` subdomain may be necessary, because this playbook could install the [Dimension integrations manager](http://dimension.t2bot.io/) for you. Dimension installation is disabled by default, because it's only possible to install it after the other Matrix services are working (see [Setting up Dimension](configuring-playbook-dimension.md) later). If you do not wish to set up Dimension, feel free to skip the `dimension.<your-domain>` DNS record.

The `jitsi.<your-domain>` subdomain may be necessary, because this playbook could install the [Jitsi video-conferencing platform](https://jitsi.org/) for you. Jitsi installation is disabled by default, because it may be heavy and is not a core required component. To learn how to install it, see our [Jitsi](configuring-playbook-jitsi.md) guide. If you do not wish to set up Jitsi, feel free to skip the `jitsi.<your-domain>` DNS record.

The `stats.<your-domain>` subdomain may be necessary, because this playbook could install [Grafana](https://grafana.com/) and setup performance metrics for you. Grafana installation is disabled by default, it is not a core required component. To learn how to install it, see our [metrics and graphs guide](configuring-playbook-prometheus-grafana.md). If you do not wish to set up Grafana, feel free to skip the `stats.<your-domain>` DNS record. It is possible to install Prometheus without installing Grafana, this would also not require the `stats.<your-domain>` subdomain.

The `goneb.<your-domain>` subdomain may be necessary, because this playbook could install the [Go-NEB](https://github.com/matrix-org/go-neb) bot. The installation of Go-NEB is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Go-NEB guide](configuring-playbook-bot-go-neb.md). If you do not wish to set up Go-NEB, feel free to skip the `goneb.<your-domain>` DNS record.

The `sygnal.<your-domain>` subdomain may be necessary, because this playbook could install the [Sygnal](https://github.com/matrix-org/sygnal) push gateway. The installation of Sygnal is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Sygnal guide](configuring-playbook-sygnal.md). If you do not wish to set up Sygnal (you probably don't, unless you're also developing/building your own Matrix apps), feel free to skip the `sygnal.<your-domain>` DNS record.

The `ntfy.<your-domain>` subdomain may be necessary, because this playbook could install the [ntfy](https://ntfy.sh/) UnifiedPush-compatible push notifications server. The installation of ntfy is disabled by default, it is not a core required component. To learn how to install it, see our [configuring ntfy guide](configuring-playbook-ntfy.md). If you do not wish to set up ntfy, feel free to skip the `ntfy.<your-domain>` DNS record.

The `etherpad.<your-domain>` subdomain may be necessary, because this playbook could install the [Etherpad](https://etherpad.org/) a highly customizable open source online editor providing collaborative editing in really real-time. The installation of etherpad is disabled by default, it is not a core required component. To learn how to install it, see our [configuring etherpad guide](configuring-playbook-etherpad.md). If you do not wish to set up etherpad, feel free to skip the `etherpad.<your-domain>` DNS record.

The `hydrogen.<your-domain>` subdomain may be necessary, because this playbook could install the [Hydrogen](https://github.com/vector-im/hydrogen-web) web client. The installation of Hydrogen is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Hydrogen guide](configuring-playbook-client-hydrogen.md). If you do not wish to set up Hydrogen, feel free to skip the `hydrogen.<your-domain>` DNS record.

The `cinny.<your-domain>` subdomain may be necessary, because this playbook could install the [Cinny](https://github.com/ajbura/cinny) web client. The installation of cinny is disabled by default, it is not a core required component. To learn how to install it, see our [configuring cinny guide](configuring-playbook-client-cinny.md). If you do not wish to set up cinny, feel free to skip the `cinny.<your-domain>` DNS record.

The `buscarron.<your-domain>` subdomain may be necessary, because this playbook could install the [buscarron](https://gitlab.com/etke.cc/buscarron) bot. The installation of buscarron is disabled by default, it is not a core required component. To learn how to install it, see our [configuring buscarron guide](configuring-playbook-bot-buscarron.md). If you do not wish to set up buscarron, feel free to skip the `buscarron.<your-domain>` DNS record.

## `_matrix-identity._tcp` SRV record setup

To make the [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server (which this playbook may optionally install for you) enable its federation features, set up an SRV record that looks like this:
- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.<your-domain>` (replace `<your-domain>` with your own)

This is an optional feature for the optionally-installed [ma1sd service](configuring-playbook-ma1sd.md). See [ma1sd's documentation](https://github.com/ma1uta/ma1sd/wiki/mxisd-and-your-privacy#choices-are-never-easy) for information on the privacy implications of setting up this SRV record.

Note: This `_matrix-identity._tcp` SRV record for the identity server is different from the `_matrix._tcp` that can be used for Synapse delegation. See [howto-server-delegation.md](howto-server-delegation.md) for more information about delegation.

When you're done with the DNS configuration and ready to proceed, continue with [Getting the playbook](getting-the-playbook.md).

## `_dmarc`, `postmoogle._domainkey` TXT and `matrix` MX records setup

To make the [postmoogle](configuring-playbook-bot-postmoogle.md) email bridge enable its email sending features, you need to configure
SPF (TXT), DMARC (TXT), DKIM (TXT) and MX records
