// Create a managed private endpoint to the databricks workspace
resource "azurerm_data_factory_managed_private_endpoint" "env_to_databricks" {
  name               = "${var.prefix}-managed_pe-adf_to_databricks"
  data_factory_id    = var.data_factory_id
  target_resource_id = var.databricks_workspace_id
  subresource_name   = "databricks_ui_api"
}

resource "azurerm_private_endpoint" "env_to_subnet" {
  name                = "${var.prefix}-pe-adf_to_subnet"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = "${var.prefix}-service_connection"
    private_connection_resource_id = var.data_factory_id
    is_manual_connection           = false
    subresource_names              = ["dataFactory", "portal"]
  }
}

resource "azurerm_data_factory_linked_service_azure_databricks" "env" {
  name            = "${var.prefix}-linked_service-databricks"
  data_factory_id = var.data_factory_id
  description     = "ADB Linked Service via AKV Access Token"

  existing_cluster_id = var.databricks_cluster_id
  adb_domain          = "https://${var.databricks_workspace_url}"

  key_vault_password {
    linked_service_name = azurerm_data_factory_linked_service_key_vault.env.name
    secret_name         = "dbw_access_token"
  }
}