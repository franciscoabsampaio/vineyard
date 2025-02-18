locals {
  dbw_is_premium = { for k, v in var.environments :
    k => v.databricks.sku == "premium"
  }
}
resource "azurerm_databricks_workspace" "env" {
  for_each = var.environments

  name                = "${local.prefix}-${each.key}-dbw"
  resource_group_name = azurerm_resource_group.env[each.key].name
  location            = azurerm_resource_group.env[each.key].location
  sku                 = each.value.databricks.sku

  public_network_access_enabled         = !each.value.databricks.private_frontend
  network_security_group_rules_required = local.dbw_is_premium[each.key] ? "NoAzureDatabricksRules" : "AllRules"

  custom_parameters {
    no_public_ip = local.dbw_is_premium[each.key]

    virtual_network_id  = azurerm_virtual_network.env[each.key].id
    public_subnet_name  = azurerm_subnet.env_public_databricks[each.key].name
    private_subnet_name = azurerm_subnet.env_private_databricks[each.key].name

    public_subnet_network_security_group_association_id  = azurerm_subnet_network_security_group_association.env_public_databricks[each.key].id
    private_subnet_network_security_group_association_id = azurerm_subnet_network_security_group_association.env_private_databricks[each.key].id
  }
}

/*
module "azuread-databricks-env" {
  source = "../modules/azuread-databricks"
  for_each = var.environments

  prefix = "${local.prefix}-${each.key}"
}
*/

module "azurerm-dbw_private_link" {
  for_each = { for k, v in var.environments :
    k => v if v.databricks.sku == "premium"
  }
  source = "../modules/azurerm-dbw_private_link"

  dbw_id                  = azurerm_databricks_workspace.env[each.key].id
  prefix                  = "${local.prefix}-${each.key}"
  resource_group_location = azurerm_resource_group.env[each.key].location
  resource_group_name     = azurerm_resource_group.env[each.key].name
  subnet_id               = azurerm_subnet.env_default[each.key].id
  vnet_id                 = azurerm_virtual_network.env[each.key].id
}