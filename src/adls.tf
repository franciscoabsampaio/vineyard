// Create only if there is no existing account
resource "azurerm_storage_account" "adls" {
  for_each = { for k, v in local.environments : k => v if !v.adls.existing_account }

  name                     = "${local.prefix}${each.key}adls"
  resource_group_name      = azurerm_resource_group.env_rg[each.key].name
  location                 = azurerm_resource_group.env_rg[each.key].location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// If a storage account already exists, and resides in its own private network
// Create a private endpoint from the default subnet to it
resource "azurerm_private_endpoint" "adls_pe" {
  for_each = { for k, v in local.environments : k => v if v.adls.existing_account && v.adls.private }

  name                = "${local.prefix}-${each.key}-adls_pe"
  location            = azurerm_resource_group.env_rg[each.key].location
  resource_group_name = azurerm_resource_group.env_rg[each.key].name

  subnet_id = azurerm_subnet.env_subnet_default[each.key].id

  private_service_connection {
    name                           = "${local.prefix}-${each.key}-adls_psc"
    private_connection_resource_id = each.value.adls.account_uri
    is_manual_connection           = false
  }
}