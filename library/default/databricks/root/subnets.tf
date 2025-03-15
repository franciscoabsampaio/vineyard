

resource "azurerm_subnet" "env_public_databricks" {
  for_each = var.environments

  name                 = "${local.prefix}-${each.key}-subnet_public_databricks"
  virtual_network_name = azurerm_virtual_network.env[each.key].name
  resource_group_name  = azurerm_resource_group.env[each.key].name
  address_prefixes     = ["10.0.2.0/24"]

  delegation {
    name = "databricks"

    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action"
      ]
    }
  }
}

resource "azurerm_subnet" "env_private_databricks" {
  for_each = var.environments

  name                 = "${local.prefix}-${each.key}-subnet_private_databricks"
  virtual_network_name = azurerm_virtual_network.env[each.key].name
  resource_group_name  = azurerm_resource_group.env[each.key].name
  address_prefixes     = ["10.0.3.0/24"]

  default_outbound_access_enabled = false

  delegation {
    name = "databricks"

    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action"
      ]
    }
  }
}

resource "azurerm_network_security_group" "env_databricks" {
  for_each = var.environments

  name                = "${local.prefix}-${each.key}-nsg_databricks"
  location            = azurerm_resource_group.env[each.key].location
  resource_group_name = azurerm_resource_group.env[each.key].name
}

resource "azurerm_subnet_network_security_group_association" "env_public_databricks" {
  for_each = var.environments

  subnet_id                 = azurerm_subnet.env_public_databricks[each.key].id
  network_security_group_id = azurerm_network_security_group.env_databricks[each.key].id
}

resource "azurerm_subnet_network_security_group_association" "env_private_databricks" {
  for_each = var.environments

  subnet_id                 = azurerm_subnet.env_private_databricks[each.key].id
  network_security_group_id = azurerm_network_security_group.env_databricks[each.key].id
}