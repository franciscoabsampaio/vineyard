# Global variables
resource_prefix = "proj"
region          = "North Europe"
repo_uri        = "https://example.com/repo.git"
subscription_id = "0000000-xxxx-xxxx-xxxx-000000000000"
private_endpoint_gateway = {
  dev  = "10.0.1.5"
  prod = "10.0.2.5"
}

# Environments
environments = {
  dev = {
    adls = {
      is_private            = true,
      existing_account      = true,
      resource_id           = "/subscriptions/0000000-xxxx-xxxx-xxxx-000000000000/resourceGroups/proj-dev-rg/providers/Microsoft.Storage/storageAccounts/xxxxxxxx",
      blob_service_endpoint = "https://xxxxxxxx.blob.core.windows.net/"
    },
    databricks = {
      sku                 = "standard", # premium
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
      existing_account = false
    },
    databricks = {
      sku                 = "standard", # premium
      cluster_node_type   = "Standard_DS3_v2",
      cluster_min_workers = 1,
      cluster_max_workers = 1
    },
    data_factory = {
      is_private = true
    }
  }
}