provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

locals {
  root = jsondecode(file("../outputs/root.json")).resources[var.env]

  env = var.environments[var.env]

  prefix = "${var.resource_prefix}-${var.env}"
}