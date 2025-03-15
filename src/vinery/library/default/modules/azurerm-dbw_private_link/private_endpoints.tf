resource "azurerm_private_endpoint" "databricks_ui_api" {
  name                = "${var.prefix}-pe-databricks_ui_api"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = "${var.prefix}-psc-databricks_ui_api"
    is_manual_connection           = false
    private_connection_resource_id = var.dbw_id
    subresource_names              = ["databricks_ui_api"]
  }

  private_dns_zone_group {
    name                 = "${var.prefix}-dns_group-databricks_ui_api"
    private_dns_zone_ids = [azurerm_private_dns_zone.databricks.id]
  }
}

resource "azurerm_private_endpoint" "databricks_browser_authentication" {
  name                = "${var.prefix}-pe-databricks_browser_authentication"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = "${var.prefix}-psc-databricks_browser_authentication"
    is_manual_connection           = false
    private_connection_resource_id = var.dbw_id
    subresource_names              = ["browser_authentication"]
  }

  private_dns_zone_group {
    name                 = "${var.prefix}-dns_group-databricks_browser_authentication"
    private_dns_zone_ids = [azurerm_private_dns_zone.databricks.id]
  }
}