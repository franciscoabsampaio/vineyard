variable "global" {}

variable "environments" {
  validation {
    condition = !anytrue([for env in var.environments :
      env.databricks.sku != "premium"
      && env.databricks.private_frontend == true
    ])
    error_message = "ERROR: Allow private frontend only if SKU is Premium tier."
  }
}