locals {
  map_of_storage_accounts = { for k, v in local.map_of_resources :
    k => v
    if split("-", k)[0] == "adls"
  }

  map_of_containers = {
    for container_details in flatten([
      for k, v in local.map_of_storage_accounts : [
        for container in v.containers :
        {
          key      = "${k}-${container}",
          name     = container,
          adls_key = k
        }
      ] if v.create_new
    ]) : container_details.key => container_details
  }
}

// Create new storage accounts
// "env_name" -> per "environment" and "name"
resource "azurerm_storage_account" "env_name" {
  for_each = { for k, v in local.map_of_storage_accounts : k => v if v.create_new }

  name                     = "${local.prefix}${each.value.environment}adls"
  resource_group_name      = azurerm_resource_group.env[each.value.environment].name
  location                 = azurerm_resource_group.env[each.value.environment].location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
// and respective containers
resource "azurerm_storage_container" "env_name_container" {
  for_each = local.map_of_containers

  name                  = each.value.name
  storage_account_id    = azurerm_storage_account.env_name[each.value.adls_key].id
  container_access_type = "private"
}

// If a storage account already exists, and resides in its own private network
// Create a private endpoint from the default subnet to it
resource "azurerm_private_endpoint" "adls" {
  for_each = { for k, v in local.map_of_storage_accounts : k => v if !v.create_new && v.is_private }

  name                = "${local.prefix}-${each.value.environment}-pe_adls_${each.value.name}"
  location            = azurerm_resource_group.env[each.value.environment].location
  resource_group_name = azurerm_resource_group.env[each.value.environment].name

  subnet_id = azurerm_subnet.env_default[each.value.environment].id

  private_service_connection {
    name                           = "${local.prefix}-${each.value.environment}-psc_adls_${each.value.name}"
    private_connection_resource_id = "${var.subscription_id}/${each.value.resource_id}"
    is_manual_connection           = false
    subresource_names              = ["blob"]
  }
}