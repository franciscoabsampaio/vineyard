// Azure Key Vault
resource "azurerm_data_factory_linked_service_key_vault" "env" {
  name            = "${var.prefix}-${var.env}-linked_service-akv"
  data_factory_id = azurerm_data_factory.env[var.env].id
  key_vault_id    = var.key_vault_id
}