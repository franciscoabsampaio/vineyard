# Terraform Framework

This project was created to be used as a plug-and-play Terraform plan that
programmatically generates an Azure data lakehouse infrastructure,
with Azure Data Factory, Azure Databricks, and an Azure Storage Account.

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