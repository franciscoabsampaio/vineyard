resource "azurerm_data_factory_linked_service_azure_blob" "adls" {
  name                = "${local.prefix}-linked_service-adls"
  data_factory_id     = azurerm_data_factory.env.id
  connection_string   = each.value.adls.existing_account ? null : azurerm_storage_account.adls[each.key].primary_blob_endpoint
  integration_runtime = "AutoResolveIntegrationRuntime"
}
