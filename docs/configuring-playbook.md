# Configuring the Ansible playbook

Once you have your server and you have [configured your DNS records](configuring-dns.md#configuring-dns), you can proceed with configuring this playbook, so that it knows what to install and where.

You can follow these steps:

- create a directory to hold your configuration (`mkdir inventory/host_vars/matrix.<your-domain>`)

- copy the sample configuration file (`cp examples/host-vars.yml inventory/host_vars/matrix.<your-domain>/vars.yml`)

- edit the configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) to your liking. You may also take a look at `roles/matrix-server/defaults.main.yml` and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

- copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

- edit the inventory hosts file (`inventory/hosts`) to your liking


For a basic Matrix installation, that's all you need.
For a more custom setup, see the [Other configuration options](#other-configuration-options) below.

When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).


## Other configuration options

- [Adjusting email-sending settings](configuring-playbook-email.md) (optional)

- [Storing Matrix media files on Amazon S3](configuring-playbook-s3.md) (optional)

- [Using an external PostgreSQL server](configuring-playbook-external-postgres.md) (optional)

- [Using your own webserver, instead of this playbook's nginx proxy](configuring-playbook-own-webserver.md) (optional)