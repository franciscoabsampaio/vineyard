module "env-data_factory" {
  source = "../modules/azurerm-adf_linked_services"

  data_factory_id = local.root.adf_id
  prefix          = local.prefix
  subnet_id       = local.root.subnet_id

  resource_group_name     = local.root.resource_group_name
  resource_group_location = local.root.resource_group_location

  adls_service_endpoint    = local.root.adls_service_endpoint
  databricks_workspace_id  = local.root.dbw_id
  databricks_workspace_url = local.root.dbw_url
  databricks_cluster_id    = databricks_cluster.env_default.id
  key_vault_id             = local.root.akv_id
}