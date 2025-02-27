<!--
SPDX-FileCopyrightText: 2018 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 André Sterba
SPDX-FileCopyrightText: 2020 Sean O'Neil
SPDX-FileCopyrightText: 2021 Martha Sokolska
SPDX-FileCopyrightText: 2022 Matt Holt
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2025 Edward Andò

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Service Discovery via .well-known

This documentation page explains how to configure Service discovery via `/.well-known/` files. Service discovery is a way for the Matrix network to discover where a Matrix server is.

## Types of well-known service discovery mechanism

There are 3 types of well-known service discovery mechanism that Matrix makes use of:

- (important) **Federation Server discovery** (`/.well-known/matrix/server`) — assists other servers in the Matrix network with finding your server. With the default playbook configuration specified on the sample `vars.yml` ([`examples/vars.yml`](../examples/vars.yml)), this is necessary for federation to work. Without a proper configuration, your server will effectively not be part of the Matrix network.

- (less important) **Client Server discovery** (`/.well-known/matrix/client`) — assists programs that you use to connect to your server (e.g. Element Web), so that they can make it more convenient for you by automatically configuring the "Homeserver URL" and "Identity Server URL" addresses.

- (optional) **Support service discovery** (`/.well-known/matrix/support`) — returns server admin contact and support page of the domain.

### Federation Server Discovery

All services created by this playbook are meant to be installed on their own server (such as `matrix.example.com`), instead of the base domain (`example.com`).

As [per the Server-Server specification](https://matrix.org/docs/spec/server_server/r0.1.0.html#server-discovery), in order to use a short Matrix user ID like `@alice:example.com` instead of `@alice:matrix.example.com` while hosting services on a subdomain such as `matrix.example.com`, the Matrix network needs to be instructed of [server delegation](howto-server-delegation.md) / redirection.

For simplicity reasons, this playbook recommends you to set up server delegation via a `/.well-known/matrix/server` file.

If you set up the DNS SRV record for server delegation instead, take a look at this documentation for more information: [Server Delegation via a DNS SRV record (advanced)](howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced)

### Client Server Discovery

Client Server Service discovery lets various client programs which support it, to receive a full user ID (e.g. `@alice:example.com`) and determine where the Matrix server is automatically (e.g. `https://matrix.example.com`).

This lets you (and your users) easily connect to your Matrix server without having to customize connection URLs. When using client programs that support it, you won't need to point them to `https://matrix.example.com` in Custom Server options manually anymore. The connection URL would be discovered automatically from your full username.

Without /.well-known/matrix/client, the client will make the wrong "homeserver URL" assumption (it will default to using https://example.com, and users will need to notice and adjust it manually (changing it to https://matrix.example.com).

As [per the Client-Server specification](https://matrix.org/docs/spec/client_server/r0.4.0.html#server-discovery) Matrix does Client Server service discovery using a `/.well-known/matrix/client` file hosted on the base domain (e.g. `example.com`).

However, this playbook installs your Matrix server on another domain (e.g. `matrix.example.com`) and not on the base domain (e.g. `example.com`), so it takes a little extra manual effort to set up the file.

### Support Service Discovery (optional)

[MSC 1929](https://github.com/matrix-org/matrix-spec-proposals/pull/1929), which was added to [Matrix Specification version v1.10](https://spec.matrix.org/v1.10/client-server-api/#getwell-knownmatrixsupport), specifies a way to add contact details of admins, as well as a link to a support page for users who are having issues with the service. Automated services may also index this information and use it for abuse reports, etc.

To enable it, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Enable generation of `/.well-known/matrix/support`.
matrix_static_files_file_matrix_support_enabled: true

# Homeserver admin contacts as per MSC 1929 https://github.com/matrix-org/matrix-spec-proposals/pull/1929
matrix_static_files_file_matrix_support_property_m_contacts:
  - matrix_id: "@admin1:{{ matrix_domain }}"
    email_address: admin@example.com
    role: m.role.admin
  - matrix_id: "@admin2:{{ matrix_domain }}"
    email_address: admin2@example.com
    role: m.role.admin
  - email_address: security@example.com
    role: m.role.security

# Your organization's support page on the base (or another) domain, if any
matrix_static_files_file_matrix_support_property_m_support_page: "https://example.com/support"
```

## Installing well-known files on the base domain's server

To implement the service discovery mechanisms, your base domain's server (e.g. `example.com`) needs to run an HTTPS-capable webserver.

### Serving the base domain from the Matrix server via the playbook

If you don't have a server for your base domain at all, you can use the Matrix server for this. If you don't need the base domain (e.g. `example.com`) for anything else (hosting a website, etc.), you can point it to the Matrix server's IP address and tell the playbook to configure it.

**This is the easiest way to set up well-known serving** — letting the playbook handle the whole base domain for you (including SSL certificates, etc.) and take care to serve the appropriate well-known files automatically.

If you decide to go this route, you don't need to read ahead in this document. Instead, go to [Serving the base domain](configuring-playbook-base-domain-serving.md) to learn how the playbook can help you set it up.

However, if you need to use the base domain for other things, this method is less suitable than the one explained below.

### Manually installing well-known files on the base domain's server

If you're managing the base domain by yourself somehow, you'll need to set up serving of some `/.well-known/matrix/*` files from it via HTTPS.

To make things easy for you to set up, this playbook generates and hosts a few well-known files on the Matrix domain's server. The files are generated at the `/matrix/static-files/public/.well-known/matrix/` path on the server and hosted at URLs like `https://matrix.example.com/.well-known/matrix/server` and `https://matrix.example.com/.well-known/matrix/client`, even though this is the wrong place to host them.

You have two options when it comes to installing the files on the base domain's server:

#### (Option 1): **Copying the files manually** to your base domain's server

**Hint**: Option 2 is generally a better way to do this. Make sure to go with it, if possible.

All you need to do is:

- copy `/.well-known/matrix/server` and `/.well-known/matrix/client` from the Matrix server (e.g. `matrix.example.com`) to your base domain's server (`example.com`). You can find these files in the `/matrix/static-files/.well-known/matrix` directory on the Matrix server. They are also accessible on URLs like this: `https://matrix.example.com/.well-known/matrix/server` (same for `client`).

- set up the server at your base domain (e.g. `example.com`) so that it adds an extra HTTP header when serving the `/.well-known/matrix/client` file. [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), the `Access-Control-Allow-Origin` header should be set with a value of `*`. If you don't do this step, web-based Matrix clients (like Element Web) may fail to work. Setting up headers for the `/.well-known/matrix/server` file is not necessary, as this file is only consumed by non-browsers, which don't care about CORS.

This is relatively easy to do and possibly your only choice if you can only host static files from the base domain's server. It is, however, **a little fragile**, as future updates performed by this playbook may regenerate the well-known files and you may need to notice that and copy them over again.

#### (Option 2): **Setting up reverse-proxying** of the well-known files from the base domain's server to the Matrix server

This option is less fragile and generally better.

On the base domain's server (e.g. `example.com`), you can set up reverse-proxying (or simply a 302 redirect), so that any access for the `/.well-known/matrix` location prefix is forwarded to the Matrix domain's server (e.g. `matrix.example.com`).

With this method, you **don't need** to add special HTTP headers for [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) reasons (like `Access-Control-Allow-Origin`), because your Matrix server (where requests ultimately go) will be configured by this playbook correctly.

**For nginx**, it would be something like this:

```nginx
# This is your HTTPS-enabled server for example.com.
server {
	server_name example.com;

	location /.well-known/matrix {
		proxy_pass https://matrix.example.com/.well-known/matrix;
		proxy_set_header X-Forwarded-For $remote_addr;
		proxy_ssl_server_name on;
	}

	# other configuration
}
```

**For Apache2**, it would be something like this:

```apache
<VirtualHost *:443>
	ServerName example.com

	SSLProxyEngine on
	ProxyPass /.well-known/matrix https://matrix.example.com/.well-known/matrix nocanon
	ProxyPassReverse /.well-known/matrix https://matrix.example.com/.well-known/matrix nocanon

	# other configuration
</VirtualHost>
```

**For Caddy 2**, it would be something like this:

```caddy
example.com {
	reverse_proxy /.well-known/matrix/* https://matrix.example.com {
		header_up Host {upstream_hostport}
	}
}
```

**For HAProxy**, it would be something like this:

```haproxy
frontend www-https
	# Select a Challenge for Matrix federation redirect
	acl matrix-acl path_beg /.well-known/matrix/
	# Use the challenge backend if the challenge is set
	use_backend matrix-backend if matrix-acl
backend matrix-backend
	# Redirects the .well-known Matrix to the Matrix server for federation.
	http-request set-header Host matrix.example.com
	server matrix matrix.example.com:80
	# Map url path as ProxyPass does
	reqirep ^(GET|POST|HEAD)\ /.well-known/matrix/(.*) \1\ /\2
	# Rewrite redirects as ProxyPassReverse does
	acl response-is-redirect res.hdr(Location) -m found
	rsprep ^Location:\ (http|https)://matrix.example.com\/(.*) Location:\ \1://matrix.example.com/.well-known/matrix/\2 if response-is-redirect
```

**For Netlify**, configure a [redirect](https://docs.netlify.com/routing/redirects/) using a `_redirects` file in the [publish directory](https://docs.netlify.com/configure-builds/overview/#definitions) with contents like this:

```
/.well-known/matrix/* https://matrix.example.com/.well-known/matrix/:splat 200!
```

**For AWS CloudFront**

   1. Add a custom origin with matrix.example.com to your distribution
   2. Add two behaviors, one for `.well-known/matrix/client` and one for `.well-known/matrix/server` and point them to your new origin.

Make sure to:

- **replace `example.com`** in the server configuration with your actual domain name
- and: to **do this for the HTTPS-enabled server block**, as that's where Matrix expects the file to be

## Confirming it works

No matter which method you've used to set up the well-known files, if you've done it correctly you should be able to see a JSON file at these URLs:

- `https://example.com/.well-known/matrix/server`
- `https://example.com/.well-known/matrix/client`
- `https://example.com/.well-known/matrix/support`

You can also check if everything is configured correctly, by [checking if services work](maintenance-and-troubleshooting.md#how-to-check-if-services-work).
