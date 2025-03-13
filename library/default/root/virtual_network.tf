resource "azurerm_virtual_network" "env" {
  name                = "${local.prefix}-${var.env}-vnet"
  location            = azurerm_resource_group.env.location
  resource_group_name = azurerm_resource_group.env.name
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  tags = {
    Environment = each.key
  }
}

resource "azurerm_subnet" "env_default" {
  name                 = "${local.prefix}-${var.env}-subnet_default"
  virtual_network_name = azurerm_virtual_network.env.name
  resource_group_name  = azurerm_resource_group.env.name
  address_prefixes     = ["10.0.1.0/24"]
}
