resource "azurerm_databricks_workspace" "env" {
  for_each = local.environments

  name                = "${local.prefix}-${each.key}-dbw"
  resource_group_name = azurerm_resource_group.env[each.key].name
  location            = azurerm_resource_group.env[each.key].location
  sku                 = each.value.databricks.sku

  public_network_access_enabled = !each.value.databricks.is_private

  # Unity Catalog and ADLS integration (default settings)
  custom_parameters {
    no_public_ip = each.value.databricks.is_private
  }
}

provider "databricks" {
  for_each = local.environments

  alias = "env"
  host  = azurerm_databricks_workspace.env[each.key].workspace_url
  azure_workspace_resource_id = azurerm_databricks_workspace.env[each.key].id
}

data "databricks_node_type" "smallest" {
  local_disk = true
  depends_on = [ azurerm_databricks_workspace.env ]
}

data "databricks_spark_version" "latest_lts" {
  long_term_support = true
}

resource "databricks_cluster" "env_default" {
  for_each = local.environments

  cluster_name            = "${local.prefix}-${each.key}-cluster-default"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 60

  autoscale {
    min_workers = each.value.databricks.min_workers
    max_workers = 1
  }
}

// If is private, create a private endpoint
resource "azurerm_private_endpoint" "databricks" {
  for_each = local.environments

  name                = "${local.prefix}-${each.key}-pe-dbw_to_subnet"
  location            = azurerm_resource_group.env[each.key].location
  resource_group_name = azurerm_resource_group.env[each.key].name
  subnet_id           = azurerm_subnet.env_subnet_default[each.key].id

  private_service_connection {
    name                           = "${local.prefix}-${each.key}-psc-dbw_to_subnet"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_databricks_workspace.env[each.key].id
    subresource_names              = ["databricks_ui_api"]
  }
}