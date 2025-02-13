provider "azurerm" {
  features {}
  subscription_id = var.global.subscription_id
}

locals {
  root = jsondecode(file("../root.json"))[var.env]

  env = var.environments[var.env]

  prefix = "${var.global.resource_prefix}-${var.env}"
}