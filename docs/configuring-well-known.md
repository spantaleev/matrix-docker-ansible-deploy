# Configuring service discovery via .well-known


## Introduction

Service discovery lets various client programs which support it, to receive a full user id (e.g. `@username:example.com`) and determine where the Matrix server is automatically (e.g. `https://matrix.example.com`).

This lets your users easily connect to your Matrix server without having to customize connection URLs.

As [per the specification](https://matrix.org/docs/spec/client_server/r0.4.0.html#server-discovery) Matrix does service discovery using a `/.well-known/matrix/client` file hosted on the base domain (e.g. `example.com`).

However, this playbook installs your Matrix server on another domain (e.g. `matrix.example.com`) and not on the base domain (e.g. `example.com`), so it takes a little extra manual effort to set up the file.


## Prerequisites

To implement service discovery, your base domain's server (e.g. `example.com`) needs to support HTTPS.


## Setting it up

To make things easy for you to set up, this playbook generates and hosts the well-known file on the Matrix domain's server (e.g. `https://matrix.example.com/.well-known/matrix/client`), even though this is the wrong place to host it.

You have 2 options when it comes to installing the file on the base domain's server:


### (Option 1): **Copying the file manually** to your base domain's server

**Hint**: Option 2 (below) is generally a better way to do this. Make sure to go with that one, if possible.

All you need to do is:

- copy the `/.well-known/matrix/client` from the Matrix server (e.g. `matrix.example.com`) to your base domain's server (`example.com`).

- set up the server at your base domain (e.g. `example.com`) so that it adds an extra HTTP header when serving the `/.well-known/matrix/client` file. [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), the `Access-Control-Allow-Origin` header should be set with a value of `*`. If you don't do this step, web-based Matrix clients (like Riot) may fail to work.

This is relatively easy to do and possibly your only choice if you can only host static files from the base domain's server.
It is, however, **a little fragile**, as future updates performed by this playbook may regenerate the well-known file and you may need to notice that and copy it again.


### (Option 2): **Setting up reverse-proxying** of the well-known file from the base domain's server to the Matrix server

This option is less fragile and generally better.

On the base domain's server (e.g. `example.com`), you can set up reverse-proxying, so that any access for the `/.well-known/matrix` location prefix is forwarded to the Matrix domain's server (e.g. `matrix.example.com`).

With this method, you **don't need** to add special HTTP headers for [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) reasons (like `Access-Control-Allow-Origin`), because your Matrix server (where requests ultimately go) will be configured by this playbook correctly.

**For nginx**, it would be something like this:

```nginx
# This is your HTTPS-enabled server for DOMAIN.
server {
	server_name DOMAIN;

	location /.well-known/matrix {
		proxy_pass https://matrix.DOMAIN/.well-known/matrix;
		proxy_set_header X-Forwarded-For $remote_addr;
	}

	# other configuration
}
```

**For Apache**, it would be something like this:

```apache
<VirtualHost *:443>
	ServerName DOMAIN

	SSLProxyEngine on
	<Location /.well-known/matrix>
		ProxyPass "https://matrix.DOMAIN/.well-known/matrix"
	</Location>

	# other configuration
</VirtualHost>
```

**For Caddy**, it would be something like this:

```caddy
proxy /.well-known/matrix https://matrix.DOMAIN
```

Make sure to:

- **replace `DOMAIN`** in the server configuration with your actual domain name
- and: to **do this for the HTTPS-enabled server block**, as that's where Matrix expects the file to be


## Confirming it works

No matter which method you've used to set up the well-known file, if you've done it correctly you should be able to see a JSON file at a URL like this: `https://<domain>/.well-known/matrix/client`.

You can also check if everything is configured correctly, by [checking if services work](maintenance-checking-services.md).
