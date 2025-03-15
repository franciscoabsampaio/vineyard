accounts = {
  alice = {
    create_new            = false,
    is_private            = true,
    resource_id           = "resourceGroups/proj-dev-rg/providers/Microsoft.Storage/storageAccounts/xxxxxxxx",
    containers            = ["container1", "container2"]
    blob_service_endpoint = "https://xxxxxxxx.blob.core.windows.net/"
  },
  bob = {
    create_new = true
    is_private = true,
    containers = ["container1", "container2"]
  }
}