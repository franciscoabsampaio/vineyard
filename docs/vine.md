# The vine CLI

## Options

### `--workspace`

When it comes to [workspace management](/README.md/#what-vineyard-is), **`vineyard`** requires all `plan` and `apply` commands to target a specific workspace, defined through the `--workspace` option (which is, by default, `default`). This allows users to ignore managing multiple workspaces if they chose to do so.

To deploy infrastructure across many environments, vine takes care of everything under the hood
they want, and even opens the door for looping CLI calls through as many environments as desired.

To enable this, **all resources** in the library include a unique environment identifier. Refer to **`vineyard`**'s [resource naming convention](./resource_name_convention.md).
