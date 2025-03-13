provider "azurerm" {
  features {}
}

locals {
  prefix = var.global.resource_prefix
}

# Loop through environments
resource "azurerm_resource_group" "env" {
  name     = "${local.prefix}-${var.env}-rg"
  location = var.global.region
}
