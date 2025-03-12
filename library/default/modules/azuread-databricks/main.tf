resource "azuread_application" "databricks" {
  display_name = "${var.prefix}-application-databricks"
}

resource "azuread_service_principal" "databricks" {
  client_id = azuread_application.databricks.client_id
}

resource "azuread_service_principal_password" "databricks" {
  service_principal_id = azuread_service_principal.databricks.id
}