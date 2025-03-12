<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Quick start

<!--
NOTE:
- Let's keep it as tidy and simple as possible.
- Because this documentation is intended to be referred by those who have not configured a Matrix server and services by using the playbook, from the educational point of view it intentionally avoids instructions based on just program's "recipes" in favor of ansible-playbook commands in most cases.
-->

This page explains how to use this Ansible playbook to install Matrix services on your server with a minimal set of core services.

We will be using `example.com` as the "base domain" in the following instruction.

By following the instruction on this page, you will set up:

- **your own Matrix server** on a `matrix.example.com` server, which is configured to present itself as `example.com`
- **your user account** like `@alice:example.com` on the server
- a **self-hosted Matrix client**, [Element Web](configuring-playbook-client-element-web.md) with the default subdomain at `element.example.com`
- Matrix delegation, so that your `matrix.example.com` server (presenting itself as `example.com`) can join the Matrix Federation and communicate with any other server in the Matrix network

Please remember to replace `example.com` with your own domain before running any commands.

## Prerequisites

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Prerequisites](prerequisites.md)</sup>

At first, **check prerequisites** and prepare for installation by setting up programs [on your own computer](prerequisites.md#your-local-computer) and [your server](prerequisites.md#server). You also need `root` access on your server (a user that could elevate to `root` via `sudo` also works).

When preparing your server, make sure to check [the server specs you need](faq.md#what-kind-of-server-specs-do-i-need). We recommend starting with a server having at least 2GB of memory.

<!--
TODO: Add one liners (or instructions, a script, etc.) for easy and consistent installation of required software. See: https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3757
-->

If you encounter an error during installation, please make sure that you have installed and configured programs correctly.

One of the main reasons of basic errors is using an incompatible version of required software such as Ansible. Take a look at [our guide about Ansible](ansible.md) for more information. In short: installing the latest available version is recommended.

## Configure your DNS settings

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Configuring DNS settings](configuring-dns.md)</sup>

After installing and configuring prerequisites, you will need to **configure DNS records**.

To configure Matrix services in the default settings, go to your DNS service provider, and adjust DNS records as below.

| Type  | Host      | Priority | Weight | Port | Target               |
| ----- | ----------| -------- | ------ | ---- | ---------------------|
| A     | `matrix`  | -        | -      | -    | `matrix-server-IPv4` |
| AAAA  | `matrix`  | -        | -      | -    | `matrix-server-IPv6` |
| CNAME | `element` | -        | -      | -    | `matrix.example.com` |

As the table illustrates, you need to create 2 subdomains (`matrix.example.com` and `element.example.com`) and point both of them to your server's IPv4/IPv6 address.

If you don't have IPv6 connectivity yet, you can skip the `AAAA` record. For more details about IPv6, see the [Configuring IPv6](./configuring-ipv6.md) documentation page.

It might take some time for the DNS records to propagate after creation.

**💡 Note**: if you are using Cloudflare DNS, make sure to disable the proxy and set all records to "DNS only"

## Get the playbook

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Getting the playbook](getting-the-playbook.md)</sup>

Next, let's **get the playbook's source code**.

We recommend to do so with [git](https://git-scm.com/) as it enables you to keep it up to date with the latest source code. While it is possible to download the playbook as a ZIP archive, it is not recommended.

To get the playbook with git, install git on your computer, go to a directory, and run the command:

```sh
git clone https://github.com/spantaleev/matrix-docker-ansible-deploy.git
```

It will fetch the playbook to a new `matrix-docker-ansible-deploy` directory underneath the directory you are currently in.

## Configure the playbook

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Configuring the playbook](configuring-playbook.md)</sup>

Now that the playbook was fetched, it is time to **configure** it per your needs.

To install Matrix services with this playbook, you would at least need 2 configuration files.

For your convenience, we have prepared example files of them ([`vars.yml`](../examples/vars.yml) and [`hosts`](../examples/hosts)).

To start quickly based on these example files, go into the `matrix-docker-ansible-deploy` directory and follow the instructions below:

1. Create a directory to hold your configuration: `mkdir -p inventory/host_vars/matrix.example.com` where `example.com` is your "base domain"
2. Copy the sample configuration file: `cp examples/vars.yml inventory/host_vars/matrix.example.com/vars.yml`
3. Copy the sample inventory hosts file: `cp examples/hosts inventory/hosts`
4. Edit the configuration file (`inventory/host_vars/matrix.example.com/vars.yml`)
5. Edit the inventory hosts file (`inventory/hosts`)

Before editing these 2 files, make sure to read explanations on them to understand what needs to be configured.

**💡 Notes:**
- If you are not in control of anything on the base domain, you would need to set additional configuration on `vars.yml`. For more information, see [How do I install on matrix.example.com without involving the base domain?](faq.md#how-do-i-install-on-matrix-example-com-without-involving-the-base-domain) on our FAQ.
- Certain configuration decisions (like the base domain configured in `matrix_domain` and homeserver implementation configured in `matrix_homeserver_implementation`) are final. If you make the wrong choice and wish to change it, you'll have to run the Uninstalling step and start over.
- Instead of configuring a lot of things all at once, we recommend starting with the basic (default) settings in order to get yourself familiar with how the playbook works. After making sure that everything works as expected, you can add (and remove) advanced settings / features and run the playbook as many times as you wish.

## Install

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Installing](installing.md)</sup>

After editing `vars.yml` and `hosts` files, let's start the **installation** procedure.

### Update Ansible roles

Before installing, you need to update the Ansible roles that this playbook uses and fetches from outside.

To update your playbook directory and all upstream Ansible roles, run:

- either: `just update`
- or: a combination of `git pull` and `just roles` (or `make roles` if you have `make` program on your computer instead of `just`)

If you don't have either `just` tool or `make` program, you can run the `ansible-galaxy` tool directly: `rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force`

### Run installation command

Then, run the command below to start installation:

````sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,ensure-matrix-users-created,start
````

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the command.

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to the command.

Wait until the command completes. If it's all green, everything should be running properly.

## Create your user account

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Registering users](registering-users.md)</sup>

As you have configured your brand new server and the client, you need to **create your user account** on your Matrix server.

To create your user account (as an administrator of the server) via this Ansible playbook, run the command below on your local computer.

**💡 Notes**:
- Make sure to adjust `YOUR_USERNAME_HERE` and `YOUR_PASSWORD_HERE`
- For `YOUR_USERNAME_HERE`, use a plain username like `alice`, not your full ID (`@alice:example.com`)

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=YOUR_USERNAME_HERE password=YOUR_PASSWORD_HERE admin=yes' --tags=register-user

# Example: ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=alice password=secret-password admin=yes' --tags=register-user
```

<!--
NOTE: detailed instruction to add users can be found on docs/registering-users.md and installing.md, which include a note about usage of admin=yes and admin=no variables. In order to keep this guide as reasonably short as possible, let's not repeat the same instruction here.
-->

## Finalize server installation

<sup>This section is optimized for this quick-start guide and is derived from the following full-documentation page: [Server Delegation](howto-server-delegation.md)</sup>

Now that you've configured Matrix services and your user account, you need to **finalize the installation process** by [setting up Matrix delegation (redirection)](howto-server-delegation.md), so that your Matrix server (`matrix.example.com`) can present itself as the base domain (`example.com`) in the Matrix network.

**This is required for federation to work!** Without a proper configuration, your server will effectively not be part of the Matrix network.

To configure the delegation, you have these two options. Choose one of them according to your situation.

- If you can afford to point the base domain at the Matrix server, follow the instruction below which guides you into [serving the base domain](configuring-playbook-base-domain-serving.md) from the integrated web server.
- Alternatively, if you're using the base domain for other purposes and cannot point it to the Matrix server (and thus cannot "serve the base domain" from it), you most likely need to [manually install well-known files on the base domain's server](configuring-well-known.md#manually-installing-well-known-files-on-the-base-domains-server).

To have the base domain served from the integrated web server, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_static_files_container_labels_base_domain_enabled: true
```

After configuring the playbook, run the command below and wait until it finishes:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-matrix-static-files,start
```

💡 Running the `install-matrix-static-files` playbook tag (as done here) is an optimized version of running [the full setup command](#run-installation-command).

After the command finishes, you can also check whether your server federates with the Matrix network by using the [Federation Tester](https://federationtester.matrix.org/) against your base domain (`example.com`), not the `matrix.example.com` subdomain.

### Re-run the full setup command any time

If you think something is wrong with the server configuration, feel free to re-run the setup command any time:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

## Log in to your user account

Finally, let's make sure that you can log in to the created account with the specified password.

You should be able to log in to it with your own [Element Web](configuring-playbook-client-element-web.md) client which you have set up at `element.example.com` by running the playbook. Open the URL (`https://element.example.com`) in a web browser and enter your credentials to log in.

**If you successfully logged in to your account, the installation and configuration have completed successfully**🎉

Come say Hi👋 in our support room — [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com). You might learn something or get to help someone else new to Matrix hosting.

## Things to do next

Once you get familiar with the playbook, you might probably want to set up additional services such as a bridge on your server.

As this page intends to be a quick start guide which explains how to start the core Matrix services, it does not cover a topic like how to set them up. Take a look at the list of [things to do next](installing.md#things-to-do-next) to learn more.

### ⚠️Keep the playbook and services up-to-date

While this playbook helps you to set up Matrix services and maintain them, it will **not** automatically run the maintenance task for you. You will need to update the playbook and re-run it **manually**.

Since it is unsafe to keep outdated services running on the server connected to the internet, please consider to update the playbook and re-run it periodically, in order to keep the services up-to-date.

For more information about upgrading or maintaining services with the playbook, take a look at this page: [Upgrading the Matrix services](maintenance-upgrading-services.md)
