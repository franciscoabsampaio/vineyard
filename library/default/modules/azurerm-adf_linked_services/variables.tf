variable "data_factory_id" {
  type = string
}

variable "prefix" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "resource_group_location" {
  type = string
}

variable "subnet_id" {
  type = string
}

// Linked Services
variable "adls_service_endpoint" {
  type = string
}

variable "databricks_workspace_id" {
  type = string
}

variable "databricks_workspace_url" {
  type = string
}

variable "databricks_cluster_id" {
  type = string
}

variable "key_vault_id" {
  type = string
}