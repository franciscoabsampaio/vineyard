resource "azurerm_databricks_workspace" "env" {
  for_each = var.environments

  name                = "${local.prefix}-${each.key}-dbw"
  resource_group_name = azurerm_resource_group.env[each.key].name
  location            = azurerm_resource_group.env[each.key].location
  sku                 = each.value.databricks.sku

  # Unity Catalog and ADLS integration (default settings)
  custom_parameters {
    no_public_ip = true

    virtual_network_id  = azurerm_virtual_network.env[each.key].id
    public_subnet_name  = azurerm_subnet.env_public_databricks[each.key].name
    private_subnet_name = azurerm_subnet.env_private_databricks[each.key].name
  }
}

/*
module "azuread-databricks-env" {
  source = "../modules/azuread-databricks"
  for_each = var.environments

  prefix = "${local.prefix}-${each.key}"
}
*/

// If is private, create a private endpoint
resource "azurerm_private_endpoint" "databricks" {
  for_each = var.environments

  name                = "${local.prefix}-${each.key}-pe-dbw_to_subnet"
  location            = azurerm_resource_group.env[each.key].location
  resource_group_name = azurerm_resource_group.env[each.key].name
  subnet_id           = azurerm_subnet.env_default[each.key].id

  private_service_connection {
    name                           = "${local.prefix}-${each.key}-psc-dbw_to_subnet"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_databricks_workspace.env[each.key].id
    subresource_names              = ["databricks_ui_api"]
  }
}