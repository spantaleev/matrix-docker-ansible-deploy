# Alternative architectures

As stated in the [Prerequisites](prerequisites.md), currently only `amd64` (`x86_64`) is fully supported.

The playbook automatically determines the target server's architecture (the `matrix_architecture` variable) to be one of the following:

- `amd64` (`x86_64`)
- `arm32`
- `arm64`

Some tools and container images can be built on the host or other measures can be used to install on that architecture.


## Implementation details

For `amd64`, prebuilt container images (see the [container images we use](container-images.md)) are used for all components (except [Hydrogen](configuring-playbook-client-hydrogen.md), which goes through self-building).

For other architecture (`arm64`, `arm32`), components which have a prebuilt image make use of it. If the component is not available for the specific architecture, [self-building](self-building.md) will be used. Not all components support self-building though, so your mileage may vary.
