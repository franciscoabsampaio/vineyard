// Create only if there is no existing account
resource "azurerm_storage_account" "env" {
  for_each = { for k, v in var.environments : k => v if !v.adls.existing_account }

  name                     = "${local.prefix}${each.key}adls"
  resource_group_name      = azurerm_resource_group.env[each.key].name
  location                 = azurerm_resource_group.env[each.key].location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// If a storage account already exists, and resides in its own private network
// Create a private endpoint from the default subnet to it
resource "azurerm_private_endpoint" "adls_pe" {
  for_each = { for k, v in var.environments : k => v if v.adls.existing_account && v.adls.is_private }

  name                = "${local.prefix}-${each.key}-adls_pe"
  location            = azurerm_resource_group.env[each.key].location
  resource_group_name = azurerm_resource_group.env[each.key].name

  subnet_id = azurerm_subnet.env_default[each.key].id

  private_service_connection {
    name                           = "${local.prefix}-${each.key}-adls_psc"
    private_connection_resource_id = each.value.adls.resource_id
    is_manual_connection           = false
    subresource_names              = ["blob"]
  }
}