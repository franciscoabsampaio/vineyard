provider "azurerm" {
  features {}

  subscription_id = "f0f49220-ade2-490c-99d5-13aaca9ac593"
}

locals {
  config_data  = jsondecode(file("../config.json"))
  environments = local.config_data.environments
  global       = local.config_data.global
  prefix       = local.global.resource_prefix

  map_of_resources = { for resource in flatten([for environment, map_of_resources in local.environments : [
    for k, v in map_of_resources : merge(v, {
      "environment"   = environment
      "resource_type" = k
    })
  ]]) : "${resource.resource_type}-${resource.environment}" => resource }
}

data "azurerm_client_config" "current" {}

# Loop through environments
resource "azurerm_resource_group" "env" {
  for_each = local.environments
  name     = "${local.prefix}-${each.key}-rg"
  location = local.global.region
}