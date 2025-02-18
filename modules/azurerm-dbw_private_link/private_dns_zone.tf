resource "azurerm_private_dns_zone" "databricks" {
  name                = "privatelink.azuredatabricks.net"
  resource_group_name = var.resource_group_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "databricks" {
  name                  = "${var.prefix}-dns_vnet_link-databricks"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.databricks.name
  virtual_network_id    = var.vnet_id
}