# Configuring your DNS settings

<sup>[Prerequisites](prerequisites.md) > Configuring your DNS settings > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md)</sup>

To set up Matrix on your domain, you'd need to do some DNS configuration.

## DNS setting for server delegation (optional)

In the sample `vars.yml` ([`examples/vars.yml`](../examples/vars.yml)), we recommend to use a short user ID like `@alice:example.com` instead of `@alice:matrix.example.com`.

To use such an ID, you don't need to install anything on the actual `example.com` server. Instead, you need to instruct the Matrix network that Matrix services for `example.com` are redirected over to `matrix.example.com`. This redirection is also known as "delegation".

As we discuss in [Server Delegation](howto-server-delegation.md), server delegation can be configured in either of these ways:

- Setting up a `/.well-known/matrix/server` file on the base domain (`example.com`)
- Setting up a `_matrix._tcp` DNS SRV record

For simplicity reasons, this playbook recommends you to set up server delegation via a `/.well-known/matrix/server` file, instead of using a DNS SRV record.

If you choose the recommended method (file-based delegation), you do not need to configure the DNS record to enable server delegation. You will need to add a necessary configuration later, when you [finalize the installation](installing.md#finalize-the-installation) after installing and starting Matrix services.

On the other hand, if you choose this method (setting up a DNS SRV record), you need to configure the additional DNS record as well as adjust SSL certificate handling. Take a look at this documentation for more information: [Server Delegation via a DNS SRV record (advanced)](howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced)

## DNS settings for services enabled by default

To serve the base domain (`example.com`) and [Element Web](configuring-playbook-client-element-web.md) with the default subdomain, adjust DNS records as below.

| Type  | Host                         | Priority | Weight | Port | Target               |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------|
| A     | `matrix`                     | -        | -      | -    | `matrix-server-IP`   |
| CNAME | `element`                    | -        | -      | -    | `matrix.example.com` |

As the table illustrates, you need to create 2 subdomains (`matrix.example.com` and `element.example.com`) and point both of them to your server's IP address (DNS `A` record or `CNAME` record is fine).

The `element.example.com` subdomain is necessary, because this playbook installs the [Element Web](https://github.com/element-hq/element-web) client for you by default. If you'd rather instruct the playbook not to install Element Web (`matrix_client_element_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `element.example.com` DNS record.

Be mindful as to how long it will take for the DNS records to propagate.

If you are using Cloudflare DNS, make sure to disable the proxy and set all records to "DNS only". Otherwise, fetching certificates will fail.

## DNS settings for optional services/features

For other services which may need subdomain settings, see the table below and configure the DNS (`CNAME`) records accordingly.

| Used by component                                                                                                          | Type  | Host                           | Priority | Weight | Port | Target                             |
| -------------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------ | -------- | ------ | ---- | -----------------------------------|
| [Dimension](configuring-playbook-dimension.md) integration server                                                          | CNAME | `dimension`                    | -        | -      | -    | `matrix.example.com`               |
| [Jitsi](configuring-playbook-jitsi.md) video-conferencing platform                                                         | CNAME | `jitsi`                        | -        | -      | -    | `matrix.example.com`               |
| [Prometheus/Grafana](configuring-playbook-prometheus-grafana.md) monitoring system                                         | CNAME | `stats`                        | -        | -      | -    | `matrix.example.com`               |
| [Go-NEB](configuring-playbook-bot-go-neb.md) bot                                                                           | CNAME | `goneb`                        | -        | -      | -    | `matrix.example.com`               |
| [Sygnal](configuring-playbook-sygnal.md) push notification gateway                                                         | CNAME | `sygnal`                       | -        | -      | -    | `matrix.example.com`               |
| [ntfy](configuring-playbook-ntfy.md) push notifications server                                                             | CNAME | `ntfy`                         | -        | -      | -    | `matrix.example.com`               |
| [Etherpad](configuring-playbook-etherpad.md) collaborative text editor                                                     | CNAME | `etherpad`                     | -        | -      | -    | `matrix.example.com`               |
| [Hydrogen](configuring-playbook-client-hydrogen.md) web client                                                             | CNAME | `hydrogen`                     | -        | -      | -    | `matrix.example.com`               |
| [Cinny](configuring-playbook-client-cinny.md) web client                                                                   | CNAME | `cinny`                        | -        | -      | -    | `matrix.example.com`               |
| [SchildiChat Web](configuring-playbook-client-schildichat-web.md) client                                                   | CNAME | `schildichat`                  | -        | -      | -    | `matrix.example.com`               |
| [wsproxy](configuring-playbook-bridge-mautrix-wsproxy.md) sms bridge                                                       | CNAME | `wsproxy`                      | -        | -      | -    | `matrix.example.com`               |
| [Buscarron](configuring-playbook-bot-buscarron.md) helpdesk bot                                                            | CNAME | `buscarron`                    | -        | -      | -    | `matrix.example.com`               |
| [rageshake](configuring-playbook-rageshake.md) bug report server                                                           | CNAME | `rageshake`                    | -        | -      | -    | `matrix.example.com`               |
| [ma1sd](configuring-playbook-ma1sd.md) identity server                                                                     | SRV   | `_matrix-identity._tcp`        | 10       | 0      | 443  | `matrix.example.com`               |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md)/[Email2Matrix](configuring-playbook-email2matrix.md) email bridges | MX    | `matrix`                       | 10       | 0      | -    | `matrix.example.com`               |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge                                                       | TXT   | `matrix`                       | -        | -      | -    | `v=spf1 ip4:matrix-server-IP -all` |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge                                                       | TXT   | `_dmarc.matrix`                | -        | -      | -    | `v=DMARC1; p=quarantine;`          |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) email bridge                                                       | TXT   | `postmoogle._domainkey.matrix` | -        | -      | -    | get it from `!pm dkim`             |

### SRV record for ma1sd

To make ma1sd enable its federation features, you need to set up a `_matrix-identity._tcp` SRV record. Don't confuse this with the `_matrix._tcp` SRV record for server delegation. See the table above and [this section](configuring-playbook-ma1sd.md#adjusting-dns-records) for values which need to be specified.

When setting up a SRV record, if you are asked for a service and protocol instead of a hostname split the host value from the table where the period is. For example use service as `_matrix-identity` and protocol as `_tcp`.

### MX and TXT records for Postmoogle

To make Postmoogle enable its email sending features, you need to configure MX and TXT (SPF, DMARC, and DKIM) records. See the table above for values which need to be specified.

---------------------------------------------

[▶️](getting-the-playbook.md) When you're done with the DNS configuration and ready to proceed, continue with [Getting the playbook](getting-the-playbook.md).
