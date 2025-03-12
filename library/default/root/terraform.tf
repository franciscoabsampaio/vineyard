terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.16.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "1.65.1"
    }
  }
}