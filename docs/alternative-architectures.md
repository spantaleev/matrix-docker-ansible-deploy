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

so for the Raspberry Pi the following should be in your `vars.yaml` file:
```
matrix_architecture = "arm32"
```

## Implementation details
This subsection is used for a reminder, how the different roles implement architecture differenes. This is **not** aimed at the users, so one does not have to do anything based on this subsection.

On most roles [self-building](self-building.md) is used if the architecture is not `amd64`, however there are some special cases:
- matrix-bridge-mautrix-facebook: there is built docker image for arm64 as well,
- matrix-bridge-mautrix-hangouts: there is built docker image for arm64 as well,
- matrix-nginx-proxy: Certbot has docker image for both arm32 and arm64, however tagging is used, which requires special handling.
