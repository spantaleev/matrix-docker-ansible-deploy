# Configuring your DNS server

<sup>⚡️[Quick start](README.md) | [Prerequisites](prerequisites.md) > Configuring your DNS server > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md) </sup>

To set up Matrix on your domain, you'd need to do some DNS configuration.

## DNS setting for server delegation (optional)

In the sample `vars.yml` ([`examples/vars.yml`](../examples/vars.yml)), we recommend to use a short user identifier like `@<username>:example.com`.

To use such an identifier, you don't need to install anything on the actual `example.com` server. Instead, you need to instruct the Matrix network that Matrix services for `example.com` are redirected over to `matrix.example.com`. This redirection is also known as "delegation".

As we discuss in [Server Delegation](howto-server-delegation.md), server delegation can be configured in either of these ways:

- Setting up a `/.well-known/matrix/server` file on the base domain (`example.com`)
- Setting up a `_matrix._tcp` DNS SRV record

For simplicity reasons, this playbook recommends you to set up server delegation via a `/.well-known/matrix/server` file, instead of using a DNS SRV record.

If you choose the recommended method (file-based delegation), you do not need to configure the DNS record to enable server delegation. You will need to add a necessary configuration later, when you [finalize the installation](installing.md#finalize-the-installation) after installing and starting Matrix services.

On the other hand, if you choose this method (setting up a DNS SRV record), you need to configure the additional DNS record as well as adjust SSL certificate handling. Take a look at this documentation for more information: [Server Delegation via a DNS SRV record (advanced)](howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced)

## DNS settings for services enabled by default

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| A     | `matrix`                     | -        | -      | -    | `matrix-server-IP`     |
| CNAME | `element`                    | -        | -      | -    | `matrix.example.com` |

Be mindful as to how long it will take for the DNS records to propagate.

If you are using Cloudflare DNS, make sure to disable the proxy and set all records to `DNS only`. Otherwise, fetching certificates will fail.

## DNS settings for optional services/features

| Used by component                                                                                                          | Type  | Host                           | Priority | Weight | Port | Target                      |
| -------------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------ | -------- | ------ | ---- | --------------------------- |
| [ma1sd](configuring-playbook-ma1sd.md) identity server                                                                     | SRV   | `_matrix-identity._tcp`        | 10       | 0      | 443  | `matrix.example.com`      |
| [Dimension](configuring-playbook-dimension.md) integration server                                                          | CNAME | `dimension`                    | -        | -      | -    | `matrix.example.com`      |
| [Jitsi](configuring-playbook-jitsi.md) video-conferencing platform                                                         | CNAME | `jitsi`                        | -        | -      | -    | `matrix.example.com`      |
| [Prometheus/Grafana](configuring-playbook-prometheus-grafana.md) monitoring system                                         | CNAME | `stats`                        | -        | -      | -    | `matrix.example.com`      |
| [Go-NEB](configuring-playbook-bot-go-neb.md) bot                                                                           | CNAME | `goneb`                        | -        | -      | -    | `matrix.example.com`      |
| [Sygnal](configuring-playbook-sygnal.md) push notification gateway                                                         | CNAME | `sygnal`                       | -        | -      | -    | `matrix.example.com`      |
| [ntfy](configuring-playbook-ntfy.md) push notifications server                                                             | CNAME | `ntfy`                         | -        | -      | -    | `matrix.example.com`      |
| [Etherpad](configuring-playbook-etherpad.md) collaborative text editor                                                     | CNAME | `etherpad`                     | -        | -      | -    | `matrix.example.com`      |
| [Hydrogen](configuring-playbook-client-hydrogen.md) web client                                                             | CNAME | `hydrogen`                     | -        | -      | -    | `matrix.example.com`      |
| [Cinny](configuring-playbook-client-cinny.md) web client                                                                   | CNAME | `cinny`                        | -        | -      | -    | `matrix.example.com`      |
| [SchildiChat Web](configuring-playbook-client-schildichat-web.md) client                                                       | CNAME | `schildichat`                  | -        | -      | -    | `matrix.example.com`      |
| [wsproxy](configuring-playbook-bridge-mautrix-wsproxy.md) sms bridge                                                       | CNAME | `wsproxy`                      | -        | -      | -    | `matrix.example.com`      |
| [Buscarron](configuring-playbook-bot-buscarron.md) helpdesk bot                                                            | CNAME | `buscarron`                    | -        | -      | -    | `matrix.example.com`      |
| [rageshake](docs/configuring-playbook-rageshake.md) bug report server                                                      | CNAME | `rageshake`                    | -        | -      | -    | `matrix.example.com`      |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md)/[Email2Matrix](configuring-playbook-email2matrix.md) email bridges | MX    | `matrix`                       | 10       | 0      | -    | `matrix.example.com`      |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge                                                       | TXT   | `matrix`                       | -        | -      | -    | `v=spf1 ip4:<your-ip> -all` |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge                                                       | TXT   | `_dmarc.matrix`                | -        | -      | -    | `v=DMARC1; p=quarantine;`   |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge                                                       | TXT   | `postmoogle._domainkey.matrix` | -        | -      | -    | get it from `!pm dkim`      |

When setting up a SRV record, if you are asked for a service and protocol instead of a hostname split the host value from the table where the period is. For example use service as `_matrix-identity` and protocol as `_tcp`.

## Subdomains setup

As the table above illustrates, you need to create 2 subdomains (`matrix.example.com` and `element.example.com`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` record is fine).

The `element.example.com` subdomain may be necessary, because this playbook installs the [Element Web](https://github.com/element-hq/element-web) client for you. If you'd rather instruct the playbook not to install Element Web (`matrix_client_element_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `element.example.com` DNS record.

The `dimension.example.com` subdomain may be necessary, because this playbook could install the [Dimension integration manager](http://dimension.t2bot.io/) for you. The installation of Dimension is disabled by default, because it's only possible to install it after the other Matrix services are working (see [Setting up Dimension integration manager](configuring-playbook-dimension.md) later). If you do not wish to set up Dimension, feel free to skip the `dimension.example.com` DNS record.

The `jitsi.example.com` subdomain may be necessary, because this playbook could install the [Jitsi video-conferencing platform](https://jitsi.org/) for you. The installation of Jitsi is disabled by default, because it may be heavy and is not a core required component. To learn how to install it, see our [Jitsi](configuring-playbook-jitsi.md) guide. If you do not wish to set up Jitsi, feel free to skip the `jitsi.example.com` DNS record.

The `stats.example.com` subdomain may be necessary, because this playbook could install [Grafana](https://grafana.com/) and setup performance metrics for you. The installation of Grafana is disabled by default, it is not a core required component. To learn how to install it, see our [metrics and graphs guide](configuring-playbook-prometheus-grafana.md). If you do not wish to set up Grafana, feel free to skip the `stats.example.com` DNS record. It is possible to install Prometheus without installing Grafana, this would also not require the `stats.example.com` subdomain.

The `goneb.example.com` subdomain may be necessary, because this playbook could install the [Go-NEB](https://github.com/matrix-org/go-neb) bot. The installation of Go-NEB is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Go-NEB guide](configuring-playbook-bot-go-neb.md). If you do not wish to set up Go-NEB, feel free to skip the `goneb.example.com` DNS record.

The `sygnal.example.com` subdomain may be necessary, because this playbook could install the [Sygnal](https://github.com/matrix-org/sygnal) push gateway. The installation of Sygnal is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Sygnal guide](configuring-playbook-sygnal.md). If you do not wish to set up Sygnal (you probably don't, unless you're also developing/building your own Matrix apps), feel free to skip the `sygnal.example.com` DNS record.

The `ntfy.example.com` subdomain may be necessary, because this playbook could install the [ntfy](https://ntfy.sh/) UnifiedPush-compatible push notifications server. The installation of ntfy is disabled by default, it is not a core required component. To learn how to install it, see our [configuring ntfy guide](configuring-playbook-ntfy.md). If you do not wish to set up ntfy, feel free to skip the `ntfy.example.com` DNS record.

The `etherpad.example.com` subdomain may be necessary, because this playbook could install the [Etherpad](https://etherpad.org/) a highly customizable open source online editor providing collaborative editing in really real-time. The installation of Etherpad is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Etherpad guide](configuring-playbook-etherpad.md). If you do not wish to set up Etherpad, feel free to skip the `etherpad.example.com` DNS record.

The `hydrogen.example.com` subdomain may be necessary, because this playbook could install the [Hydrogen](https://github.com/element-hq/hydrogen-web) web client. The installation of Hydrogen is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Hydrogen guide](configuring-playbook-client-hydrogen.md). If you do not wish to set up Hydrogen, feel free to skip the `hydrogen.example.com` DNS record.

The `cinny.example.com` subdomain may be necessary, because this playbook could install the [Cinny](https://github.com/ajbura/cinny) web client. The installation of Cinny is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Cinny guide](configuring-playbook-client-cinny.md). If you do not wish to set up Cinny, feel free to skip the `cinny.example.com` DNS record.

The `schildichat.example.com` subdomain may be necessary, because this playbook could install the [SchildiChat Web](https://github.com/SchildiChat/schildichat-desktop) client. The installation of SchildiChat Web is disabled by default, it is not a core required component. To learn how to install it, see our [configuring SchildiChat Web guide](configuring-playbook-client-schildichat-web.md). If you do not wish to set up SchildiChat Web, feel free to skip the `schildichat.example.com` DNS record.

The `wsproxy.example.com` subdomain may be necessary, because this playbook could install the [wsproxy](https://github.com/mautrix/wsproxy) web client. The installation of wsproxy is disabled by default, it is not a core required component. To learn how to install it, see our [configuring wsproxy guide](configuring-playbook-bridge-mautrix-wsproxy.md). If you do not wish to set up wsproxy, feel free to skip the `wsproxy.example.com` DNS record.

The `buscarron.example.com` subdomain may be necessary, because this playbook could install the [Buscarron](https://github.com/etkecc/buscarron) bot. The installation of Buscarron is disabled by default, it is not a core required component. To learn how to install it, see our [configuring Buscarron guide](configuring-playbook-bot-buscarron.md). If you do not wish to set up Buscarron, feel free to skip the `buscarron.example.com` DNS record.

The `rageshake.example.com` subdomain may be necessary, because this playbook could install the [rageshake](https://github.com/matrix-org/rageshake) bug report server. The installation of rageshake is disabled by default, it is not a core required component. To learn how to install it, see our [configuring rageshake guide](configuring-playbook-rageshake.md). If you do not wish to set up rageshake, feel free to skip the `rageshake.example.com` DNS record.

## `_matrix-identity._tcp` SRV record setup

To make the [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server (which this playbook may optionally install for you) enable its federation features, set up an SRV record that looks like this:
- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.example.com` (replace `example.com` with your own)

This is an optional feature for the optionally-installed [ma1sd service](configuring-playbook-ma1sd.md). See [ma1sd's documentation](https://github.com/ma1uta/ma1sd/wiki/mxisd-and-your-privacy#choices-are-never-easy) for information on the privacy implications of setting up this SRV record.

**Note**: This `_matrix-identity._tcp` SRV record for the identity server is different from the `_matrix._tcp` that can be used for Synapse delegation. See [howto-server-delegation.md](howto-server-delegation.md) for more information about delegation.

## `_dmarc`, `postmoogle._domainkey` TXT and `matrix` MX records setup

To make the [postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge enable its email sending features, you need to configure SPF (TXT), DMARC (TXT), DKIM (TXT) and MX records

---------------------------------------------

When you're done with the DNS configuration and ready to proceed, continue with [Getting the playbook](getting-the-playbook.md).
