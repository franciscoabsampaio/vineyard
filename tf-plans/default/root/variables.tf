variable "global" {}

variable "environments" {
  validation {
    condition = !anytrue([for env in var.environments :
      env.databricks.sku != "premium"
      && env.databricks.private_frontend == true
    ])
    error_message = "ERROR: Allow private frontend only if SKU is Premium tier."
  }

  validation {
    condition = anytrue([for k, v in var.environments.* :
      !contains([
        "adls",
        "databricks",
        "data_factory"
      ], split("-", k))
    ])
    error_message = "ERROR: Invalid resource type in local.tfvars"
  }
}