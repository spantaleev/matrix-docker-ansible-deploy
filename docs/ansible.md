
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

- by removing the Ansible package (`yum remove ansible` or `apt-get remove ansible`) and installing via [pip](https://pip.pypa.io/en/stable/installing/) (`pip install ansible`).

If using the `pip` method, do note that the `ansible-playbook` binary may not be on the `$PATH` (https://linuxconfig.org/linux-path-environment-variable), but in some more special location like `/usr/local/bin/ansible-playbook`. You may need to invoke it using the full path.


**Note**: Both of the above methods are a bad way to run system software such as Ansible.
If you find yourself needing to resort to such hacks, please consider reporting a bug to your distribution and/or switching to a sane distribution, which provides up-to-date software.


## Using Ansible via Docker

Alternatively, you can run Ansible on your computer from inside a Docker container (powered by the [devture/ansible](https://hub.docker.com/r/devture/ansible/) Docker image).

Here's a sample command to get you started (run this from the playbook's directory):

```bash
docker run -it --rm \
-w /work \
-v `pwd`:/work \
-v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
--entrypoint=/bin/sh \
docker.io/devture/ansible:2.9.14-r0
```

The above command tries to mount an SSH key (`$HOME/.ssh/id_rsa`) into the container (at `/root/.ssh/id_rsa`).
If your SSH key is at a different path (not in `$HOME/.ssh/id_rsa`), adjust that part.

Once you execute the above command, you'll be dropped into a `/work` directory inside a Docker container.
The `/work` directory contains the playbook's code.

You can execute `ansible-playbook` commands as per normal now.

### If you don't use SSH keys for authentication

If you don't use SSH keys for authentication, simply remove that whole line (`-v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa:ro`).
To authenticate at your server using a password, you need to add a package. So, when you are in the shell of the ansible docker container (the previously used `docker run -it ...` command), run:
```bash
apk add sshpass
```
Then, to be asked for the password whenever running an  `ansible-playbook` command add `--ask-pass` to the arguments of the command.

