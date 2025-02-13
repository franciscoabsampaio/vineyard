locals {
  output_resources = { for k, v in var.environments :
    k => {
      resource_group_name     = azurerm_resource_group.env[k].name
      resource_group_location = azurerm_resource_group.env[k].location

      subnet_id = azurerm_subnet.env_default[k].id

      adf_id = azurerm_data_factory.env[k].id
      adls_service_endpoint = (
        v.adls.existing_account ?
        v.adls.blob_service_endpoint :
        azurerm_storage_account.env[k].primary_blob_endpoint
      )
      akv_id  = azurerm_key_vault.env[k].id
      dbw_id  = azurerm_databricks_workspace.env[k].id
      dbw_url = azurerm_databricks_workspace.env[k].workspace_url
    }
  }
}

output "map_of_resources" {
  value = local.map_of_resources
}