resource "azurerm_virtual_network" "env_vnet" {
  for_each = local.environments

  name                = "${local.prefix}-${each.key}-vnet"
  location            = azurerm_resource_group.env_rg[each.key].location
  resource_group_name = azurerm_resource_group.env_rg[each.key].name
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  tags = {
    Environment = each.key
  }
}

resource "azurerm_subnet" "env_subnet_default" {
  for_each = local.environments

  name                 = "${local.prefix}-${each.key}-subnet_default"
  virtual_network_name = azurerm_virtual_network.env_vnet[each.key].name
  resource_group_name  = azurerm_resource_group.env_rg[each.key].name
  address_prefixes     = ["10.0.1.0/24"]
}

