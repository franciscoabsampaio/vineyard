resource "azurerm_key_vault" "env" {
  for_each = var.environments

  name                        = "${local.prefix}-${each.key}-akv"
  location                    = azurerm_resource_group.env[each.key].location
  resource_group_name         = azurerm_resource_group.env[each.key].name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = true

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get",
    ]

    secret_permissions = [
      "Get",
    ]

    storage_permissions = [
      "Get",
    ]
  }
}