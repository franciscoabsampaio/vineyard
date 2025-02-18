provider "databricks" {
  host = local.env.dbw_url
  # azure_use_msi = true
  azure_workspace_resource_id = azurerm_databricks_workspace.env[each.key].id
}

/*
resource "databricks_group" "infrastructure" {
  display_name = "infrastructure"
}

resource "databricks_group_member" "admin_membership" {
  group_id  = databricks_group.admins.id
  member_id = azuread_service_principal.databricks.object_id
}
*/

data "databricks_spark_version" "latest_lts" {
  long_term_support = true
}

resource "databricks_cluster" "env_default" {
  cluster_name            = "${local.prefix}-cluster-default"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = local.env.databricks.cluster_node_type
  autotermination_minutes = 60

  autoscale {
    min_workers = local.env.databricks.cluster_min_workers
    max_workers = local.env.databricks.cluster_max_workers
  }
}