<!--
SPDX-FileCopyrightText: 2026 Chiu Ki Sit

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Synology DSM

This document is a guide for preparing Synology DSM for the installation of the [Matrix Docker Ansible Deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) project.

> **Note:** Synology DSM is a community-supported platform. It is not officially tested or maintained by the project maintainers. Use at your own discretion.

**Intended audience:** Users already familiar with DSM, SSH, and this Ansible project.

## Assumptions

- DSM version 7 or higher
- `Volume1` is used as the default Docker storage location
- You are using DSM's built-in reverse proxy for handling HTTPS

## How Synology Support Works

The playbook automatically detects Synology DSM by checking for `/etc/synoinfo.conf`. When detected, it:

- Uses `synouser` and `synogroup` (DSM-native tools) instead of standard Linux user management
- Pins the Python `requests` package to a version compatible with the Docker SDK
- Deploys a `matrix-synology-boot-fix` service that runs on every boot after Docker is ready

### Boot-fix Service

Synology DSM has two boot-time quirks that the boot-fix service addresses automatically:

**1. `/volume1` shared mount propagation**

Docker requires `/volume1` to be mounted as shared (`mount --make-shared /volume1`) for container bind mounts with `bind-propagation=slave` to work correctly (used by matrix-synapse for its media store). On Synology, this cannot be inserted into the systemd chain before Container Manager starts — doing so causes Container Manager to detect a broken dependency and prompt for repair on every boot. The boot-fix service runs this command after Docker is already up, safely outside Container Manager's dependency chain.

**2. Skipped services at boot**

Synology's systemd drops services with multi-level dependency chains from the boot activation queue (e.g. `matrix-traefik → matrix-container-socket-proxy → docker`). These services show as `inactive (dead)` after reboot even though they are enabled. The boot-fix service scans for any enabled `matrix-*.service` that is still inactive after boot and starts them automatically.

> **If you previously configured a Task Scheduler entry** (`Control Panel > Task Scheduler`) to run `mount --make-shared /volume1` at boot-up, you can remove it — the boot-fix service now handles this.

## Synology GUI Preparation

1. **Enable SSH**
   - `Control Panel` > `Terminal & SNMP` > `Enable SSH service`

2. **Enable SFTP**
   - `Control Panel` > `File Service` > `FTP` > `Enable SFTP service` with default port

3. **Enable User Home Directory**
   - `Control Panel` > `User & Group` > `Advanced` > `Enable user home service`

4. **Install Container Manager**
   - Install from `Package Center`

5. **Configure Reverse Proxy**
   - `Control Panel` > `Login Portal` > `Advanced` > `Reverse Proxy`
   - Create entries for each service you enable (e.g. Matrix, Element, admin page)
   - Example entry:
     - Source: `HTTPS` / `matrix.example.com` / port `443`
     - Destination: `HTTP` / `localhost` / port `81`

## SSH Preparation

### (Optional but Recommended) Enable SSH Key Authentication

Configure key-based SSH login to avoid password prompts during Ansible runs.

### Set Up the Ansible Environment

Create a project folder and Python virtual environment on the DSM host:

```shell
mkdir ~/path/to/your/project/folder
cd ~/path/to/your/project/folder

python3 -m venv ./myenv
source ./myenv/bin/activate
```

## Inventory Configuration

In your `inventory/hosts` file, set the Python interpreter to your virtual environment:

```ini
# SSH key authentication example
matrix.example.com ansible_host=<your-dsm-ip> ansible_ssh_user=<dsm-ssh-user> become=true become_user=root ansible_python_interpreter=/absolute/path/to/myenv/bin/python ansible_sudo_pass='your-password'
```

## vars.yml Configuration

Add the following Synology-specific variables to your `vars.yml`:

```yaml
# Synology-specific settings

# User and group that will be created automatically by the playbook
matrix_user_name: "matrix"
matrix_group_name: "matrix"

# Data path on your Synology volume
matrix_base_data_path: "/volume1/docker/matrix"

# Use Synology Container Manager's Docker daemon instead of installing Docker
matrix_playbook_docker_installation_enabled: false
devture_systemd_docker_base_host_command_docker: "/usr/local/bin/docker"
devture_systemd_docker_base_docker_service_name: "pkg-ContainerManager-dockerd.service"

# Use Synology's NTP service
devture_timesync_ntpd_service: "chronyd"

# Reverse proxy settings — use HTTPS at the DSM reverse proxy level
matrix_playbook_ssl_enabled: true
traefik_config_entrypoint_web_secure_enabled: false

# Bind to localhost only — DSM reverse proxy handles public traffic
traefik_container_web_host_bind_port: '127.0.0.1:81'
matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port: '127.0.0.1:8449'

# Trust X-Forwarded-* headers from the local reverse proxy
traefik_config_entrypoint_web_forwardedHeaders_insecure: true

matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_custom:
  forwardedHeaders:
    insecure: true
```

## Running the Playbook

Before running the playbook for the first time, run this once manually to ensure `/volume1` has shared mount propagation for the initial setup:

```shell
sudo mount --make-shared /volume1
```

After the playbook runs, this is handled automatically on every subsequent boot by the `matrix-synology-boot-fix` service.

```shell
# Full setup and start
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start

# Stop all services
ansible-playbook -i inventory/hosts setup.yml --tags=stop

# Apply config changes (always include start to restart running containers)
ansible-playbook -i inventory/hosts setup.yml --tags=stop,setup-all,start
```

> **Important:** Always include `stop` before `setup-all,start` when changing configuration. Running `setup-all` alone does not restart already-running containers.

## Creating Matrix Users

After the services are running, create your first Matrix user:

```shell
# option 1:
sudo docker exec -it matrix-synapse register_new_matrix_user http://localhost:8008 -c /data/homeserver.yaml -u your_username -p your_password

# option 2:
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=your_username password=your_password admin=yes|no' --tags=register-user
```
