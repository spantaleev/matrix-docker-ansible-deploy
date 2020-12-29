# Caddyfile

This directory contains sample files that show you how to do reverse-proxying using Caddy2.

## Config

| Variable           | Function |
| ------------------ | -------- |
| tls your@email.com | Specify an email address for your [ACME account](https://caddyserver.com/docs/caddyfile/directives/tls) (but if only one email is used for all sites, we recommend the email [global option](https://caddyserver.com/docs/caddyfile/options) instead) | 
| tls                | To enable [tls](https://caddyserver.com/docs/caddyfile/directives/tls) support uncomment the lines for tls |
| Jitsi              | To enable Jitsi support uncomment the lines for Jitsi and set your data |
| log {output discard }         | No output. You can find the Options in the [Documentaton](https://caddyserver.com/docs/caddyfile/directives/log) for logging |