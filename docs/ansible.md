<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Hanno J. Gödecke
SPDX-FileCopyrightText: 2022 Kai Biebel
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Using Ansible for the playbook

This playbook is meant to be run using [Ansible](https://www.ansible.com/).

Ansible typically runs on your local computer and carries out tasks on a remote server. If your local computer cannot run Ansible, you can also run Ansible on some server somewhere (including the server you wish to install to).

## Supported Ansible versions

To manually check which version of Ansible you're on, run: `ansible --version`.

For the **best experience**, we recommend getting the **latest version of Ansible available**.

We're not sure what's the minimum version of Ansible that can run this playbook successfully. The lowest version that we've confirmed (on 2022-11-26) to be working fine is: `ansible-core` (`2.11.7`) combined with `ansible` (`4.10.0`).

If your distro ships with an Ansible version older than this, you may run into issues. Consider [Upgrading Ansible](#upgrading-ansible) or [using Ansible via Docker](#using-ansible-via-docker).

## Upgrading Ansible

Depending on your distribution, you may be able to upgrade Ansible in a few different ways:

- by using an additional repository (PPA, etc.), which provides newer Ansible versions. See instructions for [CentOS](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-rhel-centos-or-fedora), [Debian](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-debian), or [Ubuntu](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu) on the Ansible website.

- by removing the Ansible package (`yum remove ansible` or `apt-get remove ansible`) and installing via [pip](https://pip.pypa.io/en/stable/installation/) (`pip install ansible`).

If using the `pip` method, do note that the `ansible-playbook` binary may not be on the `$PATH` (https://linuxconfig.org/linux-path-environment-variable), but in some more special location like `/usr/local/bin/ansible-playbook`. You may need to invoke it using the full path.

**Note**: Both of the above methods are a bad way to run system software such as Ansible. If you find yourself needing to resort to such hacks, please consider reporting a bug to your distribution and/or switching to a sane distribution, which provides up-to-date software.

## Using Ansible via Docker

Alternatively, you can run Ansible inside a Docker container (powered by the [ghcr.io/devture/ansible](https://github.com/devture/docker-ansible/pkgs/container/ansible) Docker image).

This ensures that:

- you're using a very recent Ansible version, which is less likely to be incompatible with the playbook
- you also get access to the [agru](https://github.com/etkecc/agru) tool for quicker Ansible role installation (when running `just roles`) compared to `ansible-galaxy`

You can either [run Ansible in a container on the Matrix server itself](#running-ansible-in-a-container-on-the-matrix-server-itself) or [run Ansible in a container on another computer (not the Matrix server)](#running-ansible-in-a-container-on-another-computer-not-the-matrix-server).

### Running Ansible in a container on the Matrix server itself

To run Ansible in a (Docker) container on the Matrix server itself, you need to have a working Docker installation. Docker is normally installed by the playbook, so this may be a bit of a chicken and egg problem. To solve it:

- you **either** need to install Docker manually first. Follow [the upstream instructions](https://docs.docker.com/engine/install/) for your distribution and consider setting `matrix_playbook_docker_installation_enabled: false` in your `vars.yml` file, to prevent the playbook from installing Docker
- **or** you need to run the playbook in another way (e.g. [Running Ansible in a container on another computer (not the Matrix server)](#running-ansible-in-a-container-on-another-computer-not-the-matrix-server)) at least the first time around

Once you have a working Docker installation on the server, **clone the playbook** somewhere on the server and configure it as per usual (`inventory/hosts`, `inventory/host_vars/…`, etc.), as described in [configuring the playbook](configuring-playbook.md).

You would then need to add `ansible_connection=community.docker.nsenter` to the host line in `inventory/hosts`. This tells Ansible to connect to the "remote" machine by switching Linux namespaces with [nsenter](https://man7.org/linux/man-pages/man1/nsenter.1.html), instead of using SSH.

Alternatively, you can leave your `inventory/hosts` as is and specify the connection type in **each** `ansible-playbook` call you do later, like this: `just install-all --connection=community.docker.nsenter` (or `ansible-playbook --connection=community.docker.nsenter …`).

Run this from the playbook's directory:

```sh
docker run \
-it \
--rm \
--privileged \
--pid=host \
-w /work \
--mount type=bind,src=`pwd`,dst=/work \
--entrypoint=/bin/sh \
ghcr.io/devture/ansible:11.6.0-r0-0
```

Once you execute the above command, you'll be dropped into a `/work` directory inside a Docker container. The `/work` directory contains the playbook's code.

First, consider running `git config --global --add safe.directory /work` to [resolve directory ownership issues](#resolve-directory-ownership-issues).

Finally, you can execute `just` or `ansible-playbook …` (e.g. `ansible-playbook --connection=community.docker.nsenter …`) commands as per normal now.

### Running Ansible in a container on another computer (not the Matrix server)

Run this from the playbook's directory:

```sh
docker run \
-it \
--rm \
-w /work \
--mount type=bind,src=`pwd`,dst=/work \
--mount type=bind,src$HOME/.ssh/id_ed25519,dst=/root/.ssh/id_ed25519,ro \
--entrypoint=/bin/sh \
ghcr.io/devture/ansible:11.6.0-r0-0
```

The above command tries to mount an SSH key (`$HOME/.ssh/id_ed25519`) into the container (at `/root/.ssh/id_ed25519`). If your SSH key is at a different path (not in `$HOME/.ssh/id_ed25519`), adjust that part.

Once you execute the above command, you'll be dropped into a `/work` directory inside a Docker container. The `/work` directory contains the playbook's code.

First, consider running `git config --global --add safe.directory /work` to [resolve directory ownership issues](#resolve-directory-ownership-issues).

Finally, you execute `just` or `ansible-playbook …` commands as per normal now.

#### If you don't use SSH keys for authentication

If you don't use SSH keys for authentication, simply remove that whole line (`--mount type=bind,src$HOME/.ssh/id_ed25519,dst=/root/.ssh/id_ed25519,ro`).

To authenticate at your server using a password, you need to add a package. So, when you are in the shell of the ansible docker container (the previously used `docker run -it …` command), run:

```sh
apk add sshpass
```

Then, to be asked for the password whenever running an `ansible-playbook` command add `--ask-pass` to the arguments of the command.

#### Resolve directory ownership issues

Because you're `root` in the container running Ansible and this likely differs from the owner (your regular user account) of the playbook directory outside of the container, certain playbook features which use `git` locally may report warnings such as:

> fatal: unsafe repository ('/work' is owned by someone else)
> To add an exception for this directory, call:
>  git config --global --add safe.directory /work

These errors can be resolved by making `git` trust the playbook directory by running `git config --global --add safe.directory /work`
