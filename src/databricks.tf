resource "azurerm_databricks_workspace" "env" {
  for_each = local.environments

  name                = "${local.prefix}-${each.key}-databricks"
  resource_group_name = azurerm_resource_group.env_rg[each.key].name
  location            = azurerm_resource_group.env_rg[each.key].location
  sku = each.value.databricks.sku

  public_network_access_enabled = !each.value.databricks.private

  # Unity Catalog and ADLS integration (default settings)
  custom_parameters {
    no_public_ip = each.value.databricks.private
  }
}

provider "databricks" {
  for_each = local.environments
  host = azurerm_databricks_workspace.env[each.key].workspace_url
}

data "databricks_node_type" "smallest" {
  local_disk = true
}

data "databricks_spark_version" "latest_lts" {
  long_term_support = true
}

resource "databricks_cluster" "shared_autoscaling" {
  cluster_name            = "${local.prefix}-${each.key}-cluster-default"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 60
  autoscale {
    min_workers = local.environments
    max_workers = 1
  }
}

// If is private, create a private endpoint
resource "azurerm_private_endpoint" "databricks" {
  for_each = local.environments

  name                = "${local.prefix}-${each.key}-pe-databricks_to_subnet"
  location            = azurerm_resource_group.env[each.key].location
  resource_group_name = azurerm_resource_group.env[each.key].name
  subnet_id           = azurerm_subnet.env_subnet_default[each.key].id

  private_service_connection {
    name                           = "${local.prefix}-${each.key}-psc-databricks_to_subnet"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_databricks_workspace.env[each.key].id
    subresource_names              = ["databricks_ui_api"]
  }
}