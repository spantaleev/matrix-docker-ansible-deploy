# Setting up Cinny (optional)

This playbook can install the [Cinny](https://github.com/ajbura/cinny) Matrix web client for you.

Cinny is a web client focusing primarily on simple, elegant and secure interface. It can be installed alongside or instead of Element.

## Adjusting the playbook configuration

To enable Cinny, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_cinny_enabled: true
```

### Adjusting the Cinny URL

By default, this playbook installs Cinny on the `cinny.` subdomain (`cinny.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_client_cinny_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

While a `matrix_client_cinny_path_prefix` variable exists for tweaking the path-prefix, it's [not supported anymore](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3701), because Cinny requires an application rebuild (with a tweaked build config) to be functional under a custom path.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to a different domain (`app.example.com`) than the default one (`cinny.example.com`)
matrix_client_cinny_hostname: "app.{{ matrix_domain }}"
```

## Adjusting DNS records

Once you've decided on the domain, **you may need to adjust your DNS** records to point the Cinny domain to the Matrix server.

By default, you will need to create a CNAME record for `cinny`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've adjusted `matrix_client_cinny_hostname`, you will need to adjust your DNS configuration accordingly.

## Installing

After configuring the playbook and [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command: `just install-all` or `just setup-all`
