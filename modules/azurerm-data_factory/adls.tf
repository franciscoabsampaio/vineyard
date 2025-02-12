resource "azurerm_data_factory_linked_service_azure_blob_storage" "adls" {
  name                = "${local.prefix}-linked_service-adls"
  data_factory_id     = azurerm_data_factory.env.id
  service_endpoint    = var.adls_service_endpoint
}
