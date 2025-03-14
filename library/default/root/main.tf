provider "azurerm" {
  features {}
}

locals {
  prefix = "${var.global.resource_prefix}-${terraform.workspace}"
}

resource "azurerm_resource_group" "ws" {
  name     = "${local.prefix}-rg"
  location = var.global.region
}
