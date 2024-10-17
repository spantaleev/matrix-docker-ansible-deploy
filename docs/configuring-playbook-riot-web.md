# Configuring Riot-web (optional)

By default, this playbook **used to install** the [Riot-web](https://github.com/element-hq/riot-web) Matrix client web application.

Riot has since been [renamed to Element](https://element.io/blog/welcome-to-element/).

- to learn more about Element and its configuration, see our dedicated [Configuring Element](configuring-playbook-client-element.md) documentation page
- to learn how to migrate from Riot to Element, see [Migrating to Element](#migrating-to-element) below


## Migrating to Element

### Migrating your custom settings

If you have custom `matrix_riot_web_` variables in your `inventory/host_vars/matrix.example.com/vars.yml` file, you'll need to rename them (`matrix_riot_web_` -> `matrix_client_element_`).

Some other playbook variables (but not all) with `riot` in their name are also renamed. The playbook checks and warns if you are using the old name for some commonly used ones.


### Domain migration

We used to set up Riot at the `riot.example.com` domain. The playbook now sets up Element at `element.example.com` by default.

There are a few options for handling this:

- (**avoiding changes** - using the old `riot.example.com` domain and avoiding DNS changes) -- to keep using `riot.example.com` instead of `element.example.com`, override the domain at which the playbook serves Element: `matrix_server_fqn_element: "riot.{{ matrix_domain }}"`

- (**embracing changes** - using only `element.example.com`) - set up the `element.example.com` DNS record (see [Configuring DNS](configuring-dns.md)). You can drop the `riot.example.com` in this case.


### Re-running the playbook

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
