
# Running this playbook

This playbook is meant to be run using [Ansible](https://www.ansible.com/).

Ansible typically runs on your local computer and carries out tasks on a remote server.
If your local computer cannot run Ansible, you can also run Ansible on some server somewhere (including the server you wish to install to).


## Supported Ansible versions

Ansible 2.7.1 or newer is required ([last discussion about Ansible versions](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/743)).

Note: Ubuntu 20.04 ships with Ansible 2.9.6 which is a buggy version (see this [bug](https://bugs.launchpad.net/ubuntu/+source/ansible/+bug/1880359)), which can't be used in combination with a host running new systemd (more details in [#517](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/517), [#669](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/669)). If this problem affects you, you can: avoid running Ubuntu 20.04 on your host; run Ansible from another machine targeting your host; or try to upgrade to a newer Ansible version (see below).


## Checking your Ansible version

In most cases, you won't need to worry about the Ansible version.
The playbook will try to detect it and tell you if you're on an unsupported version.

To manually check which version of Ansible you're on, run: `ansible --version`.

If you're on an old version of Ansible, you should [upgrade Ansible to a newer version](#upgrading-ansible) or [use Ansible via Docker](#using-ansible-via-docker).


## Upgrading Ansible

Depending on your distribution, you may be able to upgrade Ansible in a few different ways:

- by using an additional repository (PPA, etc.), which provides newer Ansible versions. See instructions for [CentOS](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-rhel-centos-or-fedora), [Debian](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-debian), or [Ubuntu](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu) on the Ansible website.

- by removing the Ansible package (`yum remove ansible` or `apt-get remove ansible`) and installing via [pip](https://pip.pypa.io/en/stable/installation/) (`pip install ansible`).

If using the `pip` method, do note that the `ansible-playbook` binary may not be on the `$PATH` (https://linuxconfig.org/linux-path-environment-variable), but in some more special location like `/usr/local/bin/ansible-playbook`. You may need to invoke it using the full path.


**Note**: Both of the above methods are a bad way to run system software such as Ansible.
If you find yourself needing to resort to such hacks, please consider reporting a bug to your distribution and/or switching to a sane distribution, which provides up-to-date software.


## Using Ansible via Docker

Alternatively, you can run Ansible inside a Docker container (powered by the [devture/ansible](https://hub.docker.com/r/devture/ansible/) Docker image).

This ensures that you're using a very recent Ansible version, which is less likely to be incompatible with the playbook.

There are 2 ways to go about it:

- [Running Ansible in a container on the Matrix server itself](#running-ansible-in-a-container-on-the-matrix-server-itself)
- [Running Ansible in a container on another computer (not the Matrix server)](#running-ansible-in-a-container-on-another-computer-not-the-matrix-server)


### Running Ansible in a container on the Matrix server itself

To run Ansible in a (Docker) container on the Matrix server itself, you need to have a working Docker installation.
Docker is normally installed by the playbook, so this may be a bit of a chicken and egg problem. To solve it:

- you **either** need to install Docker manually first. Follow [the upstream instructions](https://docs.docker.com/engine/install/) for your distribution and consider setting `matrix_docker_installation_enabled: false` in your `vars.yml` file, to prevent the playbook from installing Docker
- **or** you need to run the playbook in another way (e.g. [Running Ansible in a container on another computer (not the Matrix server)](#running-ansible-in-a-container-on-another-computer-not-the-matrix-server)) at least the first time around

Once you have a working Docker installation on the server, **clone the playbook** somewhere on the server and configure it as per usual (`inventory/hosts`, `inventory/host_vars/..`, etc.), as described in [configuring the playbook](configuring-playbook.md).

You would then need to add `ansible_connection=community.docker.nsenter` to the host line in `inventory/hosts`. This tells Ansible to connect to the "remote" machine by switching Linux namespaces with [nsenter](https://man7.org/linux/man-pages/man1/nsenter.1.html), instead of using SSH.
Alternatively, you can leave your `inventory/hosts` as is and specify the connection type in **each** `ansible-playbook` call you do later, like this: `ansible-playbook --connection=community.docker.nsenter ...`

Run this from the playbook's directory:

```bash
docker run -it --rm \
--privileged \
--pid=host \
-w /work \
-v `pwd`:/work \
--entrypoint=/bin/sh \
docker.io/devture/ansible:2.13.0-r0
```

Once you execute the above command, you'll be dropped into a `/work` directory inside a Docker container.
The `/work` directory contains the playbook's code.

You can execute `ansible-playbook ...` (or `ansible-playbook --connection=community.docker.nsenter ...`) commands as per normal now.


### Running Ansible in a container on another computer (not the Matrix server)

Run this from the playbook's directory:

```bash
docker run -it --rm \
-w /work \
-v `pwd`:/work \
-v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
--entrypoint=/bin/sh \
docker.io/devture/ansible:2.13.0-r0
```

The above command tries to mount an SSH key (`$HOME/.ssh/id_rsa`) into the container (at `/root/.ssh/id_rsa`).
If your SSH key is at a different path (not in `$HOME/.ssh/id_rsa`), adjust that part.

Once you execute the above command, you'll be dropped into a `/work` directory inside a Docker container.
The `/work` directory contains the playbook's code.

You can execute `ansible-playbook ...` commands as per normal now.

#### If you don't use SSH keys for authentication

If you don't use SSH keys for authentication, simply remove that whole line (`-v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa:ro`).
To authenticate at your server using a password, you need to add a package. So, when you are in the shell of the ansible docker container (the previously used `docker run -it ...` command), run:
```bash
apk add sshpass
```
Then, to be asked for the password whenever running an  `ansible-playbook` command add `--ask-pass` to the arguments of the command.

