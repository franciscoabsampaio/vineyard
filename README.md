<div align="center">
  <img src="./docs/assets/logo.png">
</div>

**vineyard** is an [infrastructure-as-code](https://www.hashicorp.com/en/resources/what-is-infrastructure-as-code) CLI that leverages opinionated, modular, plug-and-play Terraform/OpenTofu
plans to programmatically generate data and analytics infrastructures.

## This repository supports OpenTofu and Terraform

This project was tested on:

- OpenTofu 1.9.0.
- Terraform 1.6.0.

Both are great options, but [we prefer OpenTofu](./docs/opentofu-vs-terraform.md).

## Architecture

TODO: Diagram

There are two tiers of Databricks workspaces:
- Standard. Requires a public IP.
- Premium. Allows for both public and private network implementations. In this project, premium workspaces will always generate private networking resources, such as private endpoints and private links. Regardless, users can still decide if they want to enable private frontends or not.

### root VS env

The repository and workflow are split into `root` and ``env`` for a few reasons:
- Users may want to deploy critical infrastructure (which, when destroyed, represents permanent business damage and loss of information) and non-critical environment-specific infrastructure from different environments. An example would be CI/CD pipelines in different environments, for each environment.
- Certain resources are unlikely to be redeployed/altered at a frequent rate. Others, such as cluster size, are more likely to be reconfigured.
- Sequential generation of the databricks resources per-environment would have required some very rough workarounds if dynamic `provider` blocks were not used. Using `for_each` arguments in `provider` blocks is only possible in OpenTofu 1.9.0 onwards. The Terraform version with which this repository was tested does not support dynamic `provider` blocks - and most likely no future version will.

## Pre-Requisites

This framework can only be ran in a Linux machine, a Linux virtual machine,
[WSL (Windows Subsystems for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install).

The following packages must be installed:

- [OpenTofu version 1.9 or higher](https://opentofu.org/docs/intro/install/).
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt).

## Getting Started

The first step is to clone this repository to wherever you want to execute
the framework from. This can be a local development environment, or a remote
CI/CD worker.

After cloning this repository, start by running `make init`.

???

The infrastructure is created according to user-provided configurations in
the ``config.json`` file. This file serves as the user interface, and allows
for some level of customization of the project, such as:

- Number of environments.
- Resource privacy.
- ???????

## Resource Name Convention

By default, resource names must be 24 characters or shorter, follow the
``CamelCase`` convention, as well as the following guidelines:

```js
${PREFIX}-${ENV}-${RESOURCE_TYPE}-${OPTIONAL:RESOURCE_NAME}

where

PREFIX: can be any prefix the user specifies, e.g. "org_project". Hyphens should be avoided.
ENV: the environment in which the resource is being deployed / to which it belongs.
RESOURCE_TYPE: a short indicator of the resource type, e.g. "adf", "databricks", "pe" (private endpoint), etc.
RESOURCE_NAME: an optional specifier, that can be useful when many instances of the
same resource exist in the same environment. E.g. "pe-adf_to_subnet1" designates a private endpoint that connects an Azure Data Factory instance to "subnet 1".

Example: org-dev-dbw-allin

where

PREFIX: org
ENV: dev
RESOURCE_TYPE: dbw
RESOURCE_NAME: allin
```

## Known Bugs / Issues

- Changing an existing Databricks Workspace's `public_network_access_enabled` parameter via the `private_frontend` input variable (`local.tfvars`) causes the Terraform/Tofu runtime to get stuck in `Still modifying...`. Despite the message, if the execution is interrupted, the change is successful, as re-running the plan yields `Your infrastructure matches the configuration.` and the changes can be shown to have taken effect in the workspace.