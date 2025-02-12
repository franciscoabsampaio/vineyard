// If the instance is private, create private endpoints and related resources
/*
resource "azurerm_private_dns_zone" "data_factory" {
  name                = "privatelink.datafactory.azure.com"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
}

resource "azurerm_private_dns_zone_virtual_network_link" "data_factory" {
  name                  = "example-dns-link"
  resource_group_name   = azurerm_resource_group.example.name
  private_dns_zone_name = azurerm_private_dns_zone.data_factory.name
  virtual_network_id    = azurerm_virtual_network.example.id
}

resource "azurerm_private_dns_a_record" "data_factory" {
  name                = "datafactory"
  zone_name           = azurerm_private_dns_zone.data_factory.name
  resource_group_name = azurerm_resource_group.example.name
  ttl                 = 300

  records = [azurerm_private_endpoint.data_factory.private_ip_address]
}
*/