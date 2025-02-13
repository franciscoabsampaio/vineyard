provider "azurerm" {
  features {}

  subscription_id = var.global.subscription_id
}

locals {
  prefix = var.global.resource_prefix

  map_of_resources = { for resource in flatten([for environment, map_of_resources in var.environments : [
    for k, v in map_of_resources : merge(v, {
      "environment"   = environment
      "resource_type" = k
    })
  ]]) : "${resource.resource_type}-${resource.environment}" => resource }
}

data "azurerm_client_config" "current" {}

# Loop through environments
resource "azurerm_resource_group" "env" {
  for_each = var.environments
  name     = "${local.prefix}-${each.key}-rg"
  location = var.global.region
}