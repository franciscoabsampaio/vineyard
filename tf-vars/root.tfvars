# Global variables
region          = "North Europe"
private_endpoint_gateway = {
  dev  = "10.0.1.5"
  prod = "10.0.2.5"
}

# Environments
environments = {
  dev = {
    adls = {
      is_private            = true,
      create_new      = false,
      resource_id           = "resourceGroups/proj-dev-rg/providers/Microsoft.Storage/storageAccounts/xxxxxxxx",
      blob_service_endpoint = "https://xxxxxxxx.blob.core.windows.net/"
    },
    databricks = {
      sku                 = "standard", # premium
      private_frontend    = false, # If set to true, users must connect through a VPN.
      cluster_node_type   = "Standard_DS3_v2",
      cluster_min_workers = 1,
      cluster_max_workers = 1
    },
    data_factory = {
      is_private = false
    }
  },
  prod = {
    adls = {
      is_private       = true,
      create_new = true
    },
    databricks = {
      sku                 = "standard", # premium
      private_frontend    = true, # If set to true, users must connect through a VPN.
      cluster_node_type   = "Standard_DS3_v2",
      cluster_min_workers = 1,
      cluster_max_workers = 1
    },
    data_factory = {
      is_private = true
    }
  }
}