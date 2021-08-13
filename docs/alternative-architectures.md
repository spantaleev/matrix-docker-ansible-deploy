# Alternative architectures

As stated in the [Prerequisites](prerequisites.md), currently only `x86_64` is fully supported. However, it is possible to set the target architecture, and some tools can be built on the host or other measures can be used.

To that end add the following variable to your `vars.yaml` file:

```yaml
matrix_architecture: <your-matrix-server-architecture>
```

Currently supported architectures are the following:
- `amd64` (the default)
- `arm64`
- `arm32`

so for the Raspberry Pi, the following should be in your `vars.yaml` file:

```yaml
matrix_architecture: "arm32"
```

## Implementation details

For `amd64`, prebuilt container images (see the [container images we use](container-images.md)) are used everywhere, because all images are available for this architecture.

For other architectures, components which have a prebuilt image make use of it. If the component is not available for the specific architecture, [self-building](self-building.md) will be used. Not all components support self-building though, so your mileage may vary.
