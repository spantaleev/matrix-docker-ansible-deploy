# Maintenance and Troubleshooting

## How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:
```
sudo systemctl status matrix-nginx-proxy

● matrix-nginx-proxy.service - Matrix nginx proxy server
   Loaded: loaded (/etc/systemd/system/matrix-nginx-proxy.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-11-14 19:38:35 UTC; 49min ago
```

You can see the logs by using journalctl. Example:
```
sudo journalctl -fu matrix-synapse
```

## Postgres

You can access the Postgres command line interface using the script installed on your server at `/usr/local/bin/matrix-postgres-cli`.

This playbook attempts to preserve the Postgres version it starts with. When you are ready to upgrade to a new Postgres version, read through the [guide for upgrading PostgreSQL](maintenance-upgrading-postgres.md).
