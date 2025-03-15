variable "env" {
  type = string
}

variable "region" {
  type = string
}

variable "root" {
  type = string

  validation {
    condition = var.root.sku != "premium" && var.root.private_frontend == true

    error_message = "ERROR: Allow private frontend only if SKU is Premium tier."
  }
}