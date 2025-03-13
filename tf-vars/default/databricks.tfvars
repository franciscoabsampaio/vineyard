# databricks/root
root = {
  private_endpoint_gateway = {
    dev  = "10.0.1.5"
    prod = "10.0.2.5"
  }
  workspace = {
    sku                 = "standard", # premium
    private_frontend    = false,      # If set to true, users must connect through a VPN.
    cluster_node_type   = "Standard_DS3_v2",
    cluster_min_workers = 1,
    cluster_max_workers = 1
  }
}