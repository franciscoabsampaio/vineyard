# Infrastructure-as-Code Framework

This project is a set of plug-and-play [infrastructure-as-code](https://www.hashicorp.com/en/resources/what-is-infrastructure-as-code)
plans that programmatically generate an Azure data lakehouse infrastructure,
with Azure Data Factory, Azure Databricks, and an Azure Storage Account.

## This repository supports both OpenTofu and Terraform

[OpenTofu](https://opentofu.org/) was forked from [HashiCorp Terraform](https://www.terraform.io/) and [officially endorsed by the Linux Foundation](https://www.linuxfoundation.org/press/announcing-opentofu)
in response to [HashiCorp's abrupt licensing changes to Terraform](https://opentofu.org/manifesto/).

Since, it's been growing rapidly and steadily, with both strong community and industry support, and industry giants like [Oracle have already made the switch](https://www.thestack.technology/oracle-dumps-terraform-for-opentofu/)
to Terraform's vegan alternative.

Thanks to the Linux foundation's methodologies, OpenTofu has already seen the introduction of long-awaited new features.

**Of particular interest to this repository,** the ability to use the [`for_each` argument in `provider` blocks ](https://opentofu.org/docs/language/providers/configuration/#for_each-multiple-instances-of-a-provider-configuration) as of [version 1.9](https://opentofu.org/blog/opentofu-1-9-0/),
a significant milestone over Hashicorp's Terraform,
[which repeatedly refused the feature despite frequent community requests](https://support.hashicorp.com/hc/en-us/articles/6304194229267-Using-count-or-for-each-in-Provider-Configuration). Other examples of highly requested features being ignored or outright denied are [`depends_on` arguments on ``provider`` blocks](https://github.com/hashicorp/terraform/issues/2430), [direct support for single-instance resources](https://github.com/hashicorp/terraform/issues/30221), and [DynamoDB not being required in Terraform S3 backends](https://github.com/hashicorp/terraform/issues/35625) - [two of which are scheduled for the next version of OpenTofu](https://github.com/opentofu/opentofu/milestone/11) at the time of writing.

## Architecture

TODO: Diagram

Databricks workspaces are the exception and can only be created in private network

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