<!--
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Edgars Voroboks
SPDX-FileCopyrightText: 2020 - 2021 Aaron Raimist
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2020 Rónán Duddy
SPDX-FileCopyrightText: 2021 Yannick Goossens
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Johan Swetzén
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring DNS settings

<sup>[Prerequisites](prerequisites.md) > Configuring DNS settings > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md)</sup>

To set up Matrix on your domain, you'd need to do some DNS configuration.

## DNS settings for services enabled by default

To serve the base domain (`example.com`) and [Element Web](configuring-playbook-client-element-web.md) with the default subdomain, adjust DNS records as below.

| Type  | Host      | Priority | Weight | Port | Target               |
| ----- | --------- | -------- | ------ | ---- | ---------------------|
| A     | `matrix`  | -        | -      | -    | `matrix-server-IPv4` |
| AAAA  | `matrix`  | -        | -      | -    | `matrix-server-IPv6` |
| CNAME | `element` | -        | -      | -    | `matrix.example.com` |

As the table illustrates, you need to create 2 subdomains (`matrix.example.com` and `element.example.com`) and point both of them to your server's IPv4/IPv6 address.

If you don't have IPv6 connectivity yet, you can skip the `AAAA` record. For more details about IPv6, see the [Configuring IPv6](./configuring-ipv6.md) documentation page.

The `element.example.com` subdomain is necessary, because this playbook installs the [Element Web](https://github.com/element-hq/element-web) client for you by default. If you'd rather instruct the playbook not to install Element Web (`matrix_client_element_enabled: false` when [Configuring the playbook](configuring-playbook.md) later), feel free to skip the `element.example.com` DNS record.

Be mindful as to how long it will take for the DNS records to propagate.

**Note**: if you are using Cloudflare DNS, make sure to disable the proxy and set all records to "DNS only". Otherwise, fetching certificates will fail.

## DNS setting for server delegation (optional)

In the sample `vars.yml` ([`examples/vars.yml`](../examples/vars.yml)), we recommend to use a short user ID like `@alice:example.com` instead of `@alice:matrix.example.com`.

To use such an ID, you don't need to install anything on the actual `example.com` server. Instead, you need to instruct the Matrix network that Matrix services for `example.com` are redirected over to `matrix.example.com`. This redirection is also known as "delegation".

As we discuss in [Server Delegation](howto-server-delegation.md), server delegation can be configured in either of these ways:

- Setting up a `/.well-known/matrix/server` file on the base domain (`example.com`)
- Setting up a `_matrix._tcp` DNS SRV record

For simplicity reasons, this playbook recommends you to set up server delegation via a `/.well-known/matrix/server` file, instead of using a DNS SRV record.

If you choose the recommended method (file-based delegation), you do not need to configure the DNS record to enable server delegation. You will need to add a necessary configuration later, when you [finalize the installation](installing.md#finalize-the-installation) after installing and starting Matrix services.

On the other hand, if you choose this method (setting up a DNS SRV record), you need to configure the additional DNS record as well as adjust SSL certificate handling. Take a look at this documentation for more information: [Server Delegation via a DNS SRV record (advanced)](howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced)

---------------------------------------------

[▶️](getting-the-playbook.md) When you're done with the DNS configuration and ready to proceed, continue with [Getting the playbook](getting-the-playbook.md).
