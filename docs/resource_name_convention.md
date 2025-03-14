# Resource Name Convention

By default, resource names must be 24 characters or shorter, follow the
``snake_case`` convention, as well as the following guidelines:

```js
${PREFIX}-${WORKSPACE}-${RESOURCE_TYPE}-${OPTIONAL:DESCRIPTOR}

where

PREFIX: can be any prefix the user specifies, e.g. "org_project". Hyphens should be avoided.
WORKSPACE: the workspace/environment in which the resource is being deployed / to which it belongs.
RESOURCE_TYPE: a short indicator of the resource type, e.g. "adf", "databricks", "pe" (private endpoint), etc.
DESCRIPTOR: an optional specifier, that can be useful when many instances of the
same resource exist in the same workspace. E.g. "pe-adf_to_subnet1" designates a private endpoint that connects an Azure Data Factory instance to "subnet 1".

Example: org-dev-dbw-allin

where

PREFIX: org
ENV: dev
RESOURCE_TYPE: dbw
RESOURCE_NAME: allin
```

## Resource Block Naming Convention

In our [default library](library.md), [resource blocks](https://developer.hashicorp.com/terraform/language/resources/syntax) also follow a consistent, specific naming convention, similar to the resource naming convention, but with the objective of providing clarity on how this resource fits in the larger resource tree.

At a minimum, every resource block will be named `ws`, which signifies that one instance of the resource exists per workspace.

This prefix can optionally be incremented if more than one instance is expected per workspace: `ws_descriptor1`, `ws_descriptor2`, `ws_descriptor3`, can be three separate instances that exist on every workspace.

Additionally, if resources are created with a `for_each` or `count` argument, an additional iterator parameter is expected in the resource block name: `ws_descriptor-iterator_descriptor`. Again, descriptors are optional. Here are some resource block names as examples:

- `ws_default`: the "default" resource instance for every workspace.
- `ws-adls_account`: a resource that is created for each `adls_account` in each workspace.
- `ws_databricks-subnet_default`: a resource that is created for the "databricks" instance of every workspace, and for each instance of `subnet_default`.
