locals {
  prefix = "${var.prefix}-${var.env}"
}

resource "azurerm_data_factory" "env" {
  name                = "${local.prefix}-adf"
  resource_group_name = resource_group_name
  location            = resource_group_location

  public_network_enabled = var.is_private
}
