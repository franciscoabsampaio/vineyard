resource "azurerm_virtual_network" "env" {
  for_each = var.environments

  name                = "${local.prefix}-${each.key}-vnet"
  location            = azurerm_resource_group.env[each.key].location
  resource_group_name = azurerm_resource_group.env[each.key].name
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  tags = {
    Environment = each.key
  }
}

resource "azurerm_subnet" "env_default" {
  for_each = var.environments

  name                 = "${local.prefix}-${each.key}-subnet_default"
  virtual_network_name = azurerm_virtual_network.env[each.key].name
  resource_group_name  = azurerm_resource_group.env[each.key].name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "env_public_databricks" {
  for_each = var.environments

  name                 = "${local.prefix}-${each.key}-subnet_public_databricks"
  virtual_network_name = azurerm_virtual_network.env[each.key].name
  resource_group_name  = azurerm_resource_group.env[each.key].name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_subnet" "env_private_databricks" {
  for_each = var.environments

  name                 = "${local.prefix}-${each.key}-subnet_private_databricks"
  virtual_network_name = azurerm_virtual_network.env[each.key].name
  resource_group_name  = azurerm_resource_group.env[each.key].name
  address_prefixes     = ["10.0.3.0/24"]

  default_outbound_access_enabled = false
}