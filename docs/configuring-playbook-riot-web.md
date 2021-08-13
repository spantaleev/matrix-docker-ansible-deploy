# Configuring Riot-web (optional)

By default, this playbook **used to install** the [Riot-web](https://github.com/vector-im/riot-web) Matrix client web application.

Riot has since been [renamed to Element](https://element.io/blog/welcome-to-element/).

- to learn more about Element and its configuration, see our dedicated [Configuring Element](configuring-playbook-client-element.md) documentation page
- to learn how to migrate from Riot to Element, see [Migrating to Element](#migrating-to-element) below


## Migrating to Element

### Migrating your custom settings

If you have custom `matrix_riot_web_` variables in your `inventory/host_vars/matrix.DOMAIN/vars.yml` file, you'll need to rename them (`matrix_riot_web_` -> `matrix_client_element_`).

Some other playbook variables (but not all) with `riot` in their name are also renamed. The playbook checks and warns if you are using the old name for some commonly used ones.


### Domain migration

We used to set up Riot at the `riot.DOMAIN` domain. The playbook now sets up Element at `element.DOMAIN` by default.

There are a few options for handling this:

- (**avoiding changes** - using the old `riot.DOMAIN` domain and avoiding DNS changes) -- to keep using `riot.DOMAIN` instead of `element.DOMAIN`, override the domain at which the playbook serves Element: `matrix_server_fqn_element: "riot.{{ matrix_domain }}"`

- (**embracing changes** - using only `element.DOMAIN`) - set up the `element.DOMAIN` DNS record (see [Configuring DNS](configuring-dns.md)). You can drop the `riot.DOMAIN` in this case. If so, you may also wish to remove old SSL certificates (`rm -rf /matrix/ssl/config/live/riot.DOMAIN`) and renewal configuration (`rm -f /matrix/ssl/config/renewal/riot.DOMAIN.conf`), so that `certbot` would stop trying to renew them.

- (**embracing changes and transitioning smoothly** - using both `element.DOMAIN` and `riot.DOMAIN`) - to serve Element at the new domain (`element.DOMAIN`) and to also have `riot.DOMAIN` redirect there - set up the `element.DOMAIN` DNS record (see [Configuring DNS](configuring-dns.md)) and enable Riot to Element redirection (`matrix_nginx_proxy_proxy_riot_compat_redirect_enabled: true`).


### Re-running the playbook

As always, after making the necessary DNS and configuration adjustments, re-run the playbook to apply the changes:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```
