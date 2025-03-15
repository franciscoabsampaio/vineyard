// Azure Key Vault
resource "azurerm_data_factory_linked_service_key_vault" "env" {
  name            = "${var.prefix}-linked_service-akv"
  data_factory_id = var.data_factory_id
  key_vault_id    = var.key_vault_id
}