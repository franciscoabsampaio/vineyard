module "env-data_factory" {
  for_each = local.environments

  source = "../modules/azurerm-data_factory"

  env    = each.key
  prefix = local.prefix
  is_private = each.value.is_private
  subnet_id  = azurerm_subnet.env_subnet_default[each.key].id

  resource_group_name     = azurerm_resource_group.env[each.key].name
  resource_group_location = azurerm_resource_group.env[each.key].location

  databricks_workspace_id  = azurerm_databricks_workspace.env[each.key].id
  databricks_workspace_url = azurerm_databricks_workspace.env[each.key].workspace_url
  databricks_cluster_id    = ????
  key_vault_id             = 
}