# Setting up Rageshake (optional)

The playbook can install and configure the [rageshake](https://github.com/matrix-org/rageshake) bug report server for you.

This is useful if you're developing your own applications and would like to collect bug reports for them.

## Adjusting the playbook configuration

To enable Rageshake, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_rageshake_enabled: true
```

Rageshake has various options which don't have dedicated Ansible variables. You can see the full list of options in the [`rageshake.sample.yaml` file](https://github.com/matrix-org/rageshake/blob/master/rageshake.sample.yaml).

To set these, you can make use of the  `matrix_rageshake_configuration_extension_yaml` variable like this:

```yaml
matrix_rageshake_configuration_extension_yaml: |
  github_token: secrettoken

  github_project_mappings:
     my-app: octocat/HelloWorld
```

### Adjusting the Rageshake URL

By default, this playbook installs Rageshake on the `rageshake.` subdomain (`rageshake.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_rageshake_hostname` and `matrix_rageshake_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Rageshake.
matrix_rageshake_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /rageshake subpath
matrix_rageshake_path_prefix: /rageshake
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Rageshake domain to the Matrix server.

By default, you will need to create a CNAME record for `rageshake`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

Refer to the [rageshake documentation](https://github.com/matrix-org/rageshake) for available APIs, etc.
