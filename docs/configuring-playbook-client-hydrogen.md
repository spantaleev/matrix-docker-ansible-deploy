# Setting up Hydrogen (optional)

This playbook can install the [Hydrogen](https://github.com/element-hq/hydrogen-web) Matrix web client for you.

Hydrogen is a lightweight web client that supports mobile and legacy web browsers. It can be installed alongside or instead of Element Web.

## Adjusting the playbook configuration

To enable Hydrogen, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_hydrogen_enabled: true
```

### Adjusting the Hydrogen URL

By default, this playbook installs Hydrogen on the `hydrogen.` subdomain (`hydrogen.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_client_hydrogen_hostname` and `matrix_client_hydrogen_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Hydrogen.
matrix_client_hydrogen_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /hydrogen subpath
matrix_client_hydrogen_path_prefix: /hydrogen
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Hydrogen domain to the Matrix server.

By default, you will need to create a CNAME record for `hydrogen`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)
