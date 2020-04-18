# Alternative architectures
As stated in the [Prerequisites](prerequisites.md), currently only x86_64 is supported. However, it is possible to set the target architecture, and some tools can be built on the host or other measures can be used.

To that end add the following variable to your `vars.yaml` file:
```
matrix_architecture = <your-matrix-server-architecture>
```
Currently supported architectures are the following:
- `amd64` (the default)
- `arm64`
- `arm32`

On most roles self-building is used if the architecture is not `amd64`. Special cases:
- matrix-bridge-mautrix-facebook: there is built docker image for arm64 as well,
- matrix-bridge-mautrix-hangouts: there is built docker image for arm64 as well,
- matrix-nginx-proxy: Certbot has docker image for both arm32 and arm64, however tagging is used, which requires special handling.
