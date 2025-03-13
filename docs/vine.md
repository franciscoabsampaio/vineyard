# The vine CLI

## Options

### `--env`

By default, **vineyard** supports environments, and all `plan` and `apply` commands require the `--env` option. This allows users to deploy infrastructure across however many environments they want, and even opens the door for looping CLI calls through as many environments as desired.

To enable this, **all resources** in the library include a unique environment identifier. Refer to **vineyard**'s [resource naming convention](./resource_name_convention.md).
