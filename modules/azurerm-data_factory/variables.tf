variable "env" {
  type = string
}

variable "prefix" {
  type = string
}

variable "is_private" {
  type = bool
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