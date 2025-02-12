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

By default, resources follow the following naming convention:

```js
${PREFIX}-${ENV}-${RESOURCE_TYPE}-${OPTIONAL:RESOURCE_NAME}

where

PREFIX: can be any prefix the user specifies, e.g. "Organization-Project".
ENV: the environment in which the resource is being deployed / to which it belongs.
RESOURCE_TYPE: a short indicator of the resource type, e.g. "adf", "databricks", "pe" (private endpoint), etc.
RESOURCE_NAME: an optional specifier, that can be useful when many instances of the
same resource exist in the same environment. E.g. "pe-adf_to_subnet1" designates a private endpoint that connects an Azure Data Factory instance to "subnet 1".
```