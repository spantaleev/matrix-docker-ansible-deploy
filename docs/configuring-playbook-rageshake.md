# Setting up the rageshake bug report server (optional)

The playbook can install and configure the [rageshake](https://github.com/matrix-org/rageshake) bug report server for you.

This is useful if you're developing your own applications and would like to collect bug reports for them.

## Adjusting the playbook configuration

To enable rageshake, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_rageshake_enabled: true
```

rageshake has various options which don't have dedicated Ansible variables. You can see the full list of options in the [`rageshake.sample.yaml` file](https://github.com/matrix-org/rageshake/blob/master/rageshake.sample.yaml).

To set these, you can make use of the  `matrix_rageshake_configuration_extension_yaml` variable like this:

```yaml
matrix_rageshake_configuration_extension_yaml: |
  github_token: secrettoken

  github_project_mappings:
     my-app: octocat/HelloWorld
```

### Adjusting the rageshake URL

By default, this playbook installs rageshake on the `rageshake.` subdomain (`rageshake.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_rageshake_hostname` and `matrix_rageshake_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for rageshake.
matrix_rageshake_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /rageshake subpath
matrix_rageshake_path_prefix: /rageshake
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the rageshake domain to the Matrix server.

By default, you will need to create a CNAME record for `rageshake`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Refer to the [rageshake documentation](https://github.com/matrix-org/rageshake) for available APIs, etc.
