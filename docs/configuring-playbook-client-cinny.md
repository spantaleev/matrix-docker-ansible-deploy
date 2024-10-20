# Configuring Cinny (optional)

This playbook can install the [cinny](https://github.com/ajbura/cinny) Matrix web client for you.

Cinny is a web client focusing primarily on simple, elegant and secure interface. It can be installed alongside or instead of Element.

## Adjusting the playbook configuration

To enable Cinny, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_cinny_enabled: true
```

### Adjusting the Cinny URL

By default, this playbook installs Cinny on the `cinny.` subdomain (`cinny.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_client_cinny_hostname` and `matrix_client_cinny_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Cinny.
matrix_client_cinny_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /cinny subpath
matrix_client_cinny_path_prefix: /cinny
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Cinny domain to the Matrix server.

By default, you will need to create a CNAME record for `cinny`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
