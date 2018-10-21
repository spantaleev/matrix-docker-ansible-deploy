# Configuring your DNS server

To set up Matrix on your domain, you'd need to do some DNS configuration.

To use an identifier like `@<username>:<your-domain>`, you don't actually need
to install anything on the actual `<your-domain>` server.

All services created by this playbook are meant to be installed on their own server (such as `matrix.<your-domain>`).

To accomplish such a "redirect", you need to instruct the Matrix network of this by setting up a DNS SRV record.
The SRV record should look like this:
- Name: `_matrix._tcp` (use this text as-is)
- Content: `10 0 8448 matrix.<your-domain>` (replace `<your-domain>` with your own)

To make the [mxisd](https://github.com/kamax-io/mxisd) Identity Server (which this playbook installs for you) be authoritative for your domain name, set up one more SRV record that looks like this:
- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.<your-domain>` (replace `<your-domain>` with your own)

Once you've set up these DNS SRV records, you should create 2 other domain names (`matrix.<your-domain>` and `riot.<your-domain>`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` is fine).

This playbook can then install all the services on that new server and you'll be able to join the Matrix network as `@<username>:<your-domain>`.

| Type | Host                    | Priority | Weight | Port | Target                 |
| ---- | ----------------------- | -------- | ------ | ---- | ---------------------- |
| SRV  | `_matrix._tcp`          | 10       | 0      | 8448 | `matrix.<your-domain>` |
| SRV  | `_matrix-identity._tcp` | 10       | 0      | 443  | `matrix.<your-domain>` |
| A    | `matrix`                | -        | -      | -    | `server-IP`            |
| A    | `riot`                  | -        | -      | -    | `server-IP`            |

When ready to proceed, continue with [Configuring this Ansible playbook](configuring-playbook.md).