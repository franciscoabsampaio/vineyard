resource "azurerm_data_factory_linked_service_azure_blob_storage" "adls" {
  name             = "${var.prefix}-linked_service-adls"
  data_factory_id  = var.data_factory_id
  service_endpoint = var.adls_service_endpoint
}
