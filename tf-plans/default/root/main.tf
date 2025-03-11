provider "azurerm" {
  features {}

  subscription_id = var.global.subscription_id
}

locals {
  prefix = var.global.resource_prefix

  map_of_resources = { for resource in flatten([for environment, resources in var.environments : [
    for k, v in resources : merge(v, {
      "environment"   = environment
      "resource_name" = k
      "resource_type" = split("-", k)
    })
  ]]) : "${resource.environment}-${resource.resource_name}" => resource }
}

data "azurerm_client_config" "current" {}

# Loop through environments
resource "azurerm_resource_group" "env" {
  for_each = var.environments
  name     = "${local.prefix}-${each.key}-rg"
  location = var.global.region
}