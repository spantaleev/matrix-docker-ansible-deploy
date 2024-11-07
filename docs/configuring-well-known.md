# Configuring Service Discovery via .well-known

Service discovery is a way for the Matrix network to discover where a Matrix server is.

There are 2 types of well-known service discovery that Matrix makes use of:

- (important) **Federation Server discovery** (`/.well-known/matrix/server`) -- assists other servers in the Matrix network with finding your server. Without a proper configuration, your server will effectively not be part of the Matrix network. Learn more in [Introduction to Federation Server Discovery](#introduction-to-federation-server-discovery)

- (not that important) **Client Server discovery** (`/.well-known/matrix/client`) -- assists programs that you use to connect to your server (e.g. Element Web), so that they can make it more convenient for you by automatically configuring the "Homeserver URL" and "Identity Server URL" addresses. Learn more in [Introduction to Client Server Discovery](#introduction-to-client-server-discovery)


## Introduction to Federation Server Discovery

All services created by this playbook are meant to be installed on their own server (such as `matrix.example.com`).

As [per the Server-Server specification](https://matrix.org/docs/spec/server_server/r0.1.0.html#server-discovery), to use a Matrix user identifier like `@<username>:example.com` while hosting services on a subdomain like `matrix.example.com`, the Matrix network needs to be instructed of such delegation/redirection.

Server delegation can be configured using DNS SRV records or by setting up a `/.well-known/matrix/server` file on the base domain (`example.com`).

Both methods have their place and will continue to do so. You only need to use just one of these delegation methods. For simplicity reasons, our setup advocates for the `/.well-known/matrix/server` method and guides you into using that.

To learn how to set up `/.well-known/matrix/server`, read the Installing section below.


## Introduction to Client Server Discovery

Client Server Service discovery lets various client programs which support it, to receive a full user ID (e.g. `@username:example.com`) and determine where the Matrix server is automatically (e.g. `https://matrix.example.com`).

This lets you (and your users) easily connect to your Matrix server without having to customize connection URLs. When using client programs that support it, you won't need to point them to `https://matrix.example.com` in Custom Server options manually anymore. The connection URL would be discovered automatically from your full username.

As [per the Client-Server specification](https://matrix.org/docs/spec/client_server/r0.4.0.html#server-discovery) Matrix does Client Server service discovery using a `/.well-known/matrix/client` file hosted on the base domain (e.g. `example.com`).

However, this playbook installs your Matrix server on another domain (e.g. `matrix.example.com`) and not on the base domain (e.g. `example.com`), so it takes a little extra manual effort to set up the file.

To learn how to set it up, read the Installing section below.


## (Optional) Introduction to Homeserver Admin Contact and Support page

[MSC 1929](https://github.com/matrix-org/matrix-spec-proposals/pull/1929) specifies a way to add contact details of admins, as well as a link to a support page for users who are having issues with the service. Automated services may also index this information and use it for abuse reports, etc.

The two playbook variables that you could look for, if you're interested in being an early adopter, are: `matrix_static_files_file_matrix_support_property_m_contacts` and `matrix_static_files_file_matrix_support_property_m_support_page`.

Example snippet for `vars.yml`:

```
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

To learn how to set up `/.well-known/matrix/support` for the base domain, read the Installing section below.


## Installing well-known files on the base domain's server

To implement the two service discovery mechanisms, your base domain's server (e.g. `example.com`) needs to run an HTTPS-capable webserver.

If you don't have a server for your base domain at all, you can use the Matrix server for this. See [Serving the base domain](configuring-playbook-base-domain-serving.md) to learn how the playbook can help you set it up. If you decide to go this route, you don't need to read ahead in this document. When **Serving the base domain**, the playbook takes care to serve the appropriate well-known files automatically.

If you're managing the base domain by yourself somehow, you'll need to set up serving of some `/.well-known/matrix/*` files from it via HTTPS.

To make things easy for you to set up, this playbook generates and hosts 2 well-known files on the Matrix domain's server. The files are generated at `/matrix/static-files/.well-known/matrix/` and hosted at `https://matrix.example.com/.well-known/matrix/server` and `https://matrix.example.com/.well-known/matrix/client`, even though this is the wrong place to host them.

You have 3 options when it comes to installing the files on the base domain's server:


### (Option 1): **Copying the files manually** to your base domain's server

**Hint**: Option 2 and 3 (below) are generally a better way to do this. Make sure to go with them, if possible.

All you need to do is:

- copy `/.well-known/matrix/server` and `/.well-known/matrix/client` from the Matrix server (e.g. `matrix.example.com`) to your base domain's server (`example.com`). You can find these files in the `/matrix/static-files/.well-known/matrix` directory on the Matrix server. They are also accessible on URLs like this: `https://matrix.example.com/.well-known/matrix/server` (same for `client`).

- set up the server at your base domain (e.g. `example.com`) so that it adds an extra HTTP header when serving the `/.well-known/matrix/client` file. [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), the `Access-Control-Allow-Origin` header should be set with a value of `*`. If you don't do this step, web-based Matrix clients (like Element Web) may fail to work. Setting up headers for the `/.well-known/matrix/server` file is not necessary, as this file is only consumed by non-browsers, which don't care about CORS.

This is relatively easy to do and possibly your only choice if you can only host static files from the base domain's server. It is, however, **a little fragile**, as future updates performed by this playbook may regenerate the well-known files and you may need to notice that and copy them over again.


### (Option 2): **Serving the base domain** from the Matrix server via the playbook

If you don't need the base domain (e.g. `example.com`) for anything else (hosting a website, etc.), you can point it to the Matrix server's IP address and tell the playbook to configure it.

This is the easiest way to set up well-known serving -- letting the playbook handle the whole base domain for you (including SSL certificates, etc.). However, if you need to use the base domain for other things (such as hosting some website, etc.), going with Option 1 or Option 3 might be more suitable.

See [Serving the base domain](configuring-playbook-base-domain-serving.md) to learn how the playbook can help you set it up.


### (Option 3): **Setting up reverse-proxying** of the well-known files from the base domain's server to the Matrix server

This option is less fragile and generally better.

On the base domain's server (e.g. `example.com`), you can set up reverse-proxying, so that any access for the `/.well-known/matrix` location prefix is forwarded to the Matrix domain's server (e.g. `matrix.example.com`).

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

You can also check if everything is configured correctly, by [checking if services work](maintenance-checking-services.md).
