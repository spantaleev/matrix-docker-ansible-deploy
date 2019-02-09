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

See the dedicated [PostgreSQL Maintenance](maintenances-postgres.md) documentation page.
