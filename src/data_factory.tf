module "env-data_factory" {
  for_each = local.environments

  source = "../modules/azurerm-data_factory"

  env        = each.key
  prefix     = local.prefix
  is_private = each.value.data_factory.is_private
  subnet_id  = azurerm_subnet.env_subnet_default[each.key].id

  resource_group_name     = azurerm_resource_group.env[each.key].name
  resource_group_location = azurerm_resource_group.env[each.key].location

  adls_service_endpoint   = (
    each.value.adls.existing_account ?
    each.value.adls.blob_service_endpoint :
    azurerm_storage_account.env[each.key].primary_blob_endpoint
  )
  databricks_workspace_id  = azurerm_databricks_workspace.env[each.key].id
  databricks_workspace_url = azurerm_databricks_workspace.env[each.key].workspace_url
  databricks_cluster_id    = databricks_cluster.env_default[each.key].id
  key_vault_id             = azurerm_key_vault.env[each.key].id
}