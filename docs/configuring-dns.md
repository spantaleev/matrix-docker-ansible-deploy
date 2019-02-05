# Configuring your DNS server

To set up Matrix on your domain, you'd need to do some DNS configuration.

To use an identifier like `@<username>:<your-domain>`, you don't actually need
to install anything on the actual `<your-domain>` server.


## General outline of DNS settings you need to do

| Type  | Host                    | Priority | Weight | Port | Target                 |
| ----- | ----------------------- | -------- | ------ | ---- | ---------------------- |
| A     | `matrix`                | -        | -      | -    | `matrix-server-IP`     |
| CNAME | `riot`                  | -        | -      | -    | `matrix.<your-domain>` |
| SRV   | `_matrix._tcp`          | 10       | 0      | 8448 | `matrix.<your-domain>` |
| SRV   | `_matrix-identity._tcp` | 10       | 0      | 443  | `matrix.<your-domain>` |

The `_matrix._tcp` SRV record is a temporary measure and will not be necessary in the near future.
In fact, it will have to be removed at some point. To learn more about that, read below.


## Subdomains setup

As the table above illustrates, you need to create 2 subdomains (`matrix.<your-domain>` and `riot.<your-domain>`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` record is fine).

The `riot.<your-domain>` subdomain is necessary, because this playbook installs the Riot web client for you.
If you'd rather instruct the playbook not to install Riot (`matrix_riot_web_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `riot.<your-domain>` DNS record.


## `_matrix._tcp` SRV record setup (temporary requirement)

All services created by this playbook are meant to be installed on their own server (such as `matrix.<your-domain>`).

To use a Matrix user identifier like `@<username>:<your-domain>` while hosting services on `matrix.<your-domain>`, we need to instruct the Matrix network of such a delegation/redirection by means of setting up a DNS SRV record.

The SRV record should look like this:
- Name: `_matrix._tcp` (use this text as-is)
- Content: `10 0 8448 matrix.<your-domain>` (replace `<your-domain>` with your own)

A [new file-based mechanism for Federation Server Discovery](configuring-well-known.md#introduction-to-federation-server-discovery) is superseding the `_matrix._tcp` SRV record. **During the transition phase, you'll need to set up both mechanisms**. We'll instruct you how to set up the file-based mechanism after the [installation phase](installing.md) for this playbook.

Doing delegation/redirection of Matrix services using a DNS SRV record (`_matrix._tcp`) is a **temporary measure** that is only necessary before Synapse v1.0 is released.

As more and more people upgrade to the Synapse v0.99 transitional release and just before the final Synapse v1.0 gets released, at some point in the near future **you will need to remove the `_matrix._tcp` SRV record** and leave only the [new file-based mechanism for Federation Server Discovery](configuring-well-known.md#introduction-to-federation-server-discovery) in place.


## `_matrix-identity._tcp` SRV record setup

To make the [mxisd](https://github.com/kamax-io/mxisd) Identity Server (which this playbook installs for you) be authoritative for your domain name, set up one more SRV record that looks like this:
- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.<your-domain>` (replace `<your-domain>` with your own)


When you're done with the DNS configuration and ready to proceed, continue with [Configuring this Ansible playbook](configuring-playbook.md).
