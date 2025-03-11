resource "azurerm_data_factory" "env" {
  for_each            = var.environments
  name                = "${local.prefix}-${each.key}-adf"
  resource_group_name = azurerm_resource_group.env[each.key].name
  location            = azurerm_resource_group.env[each.key].location

  public_network_enabled = each.value.data_factory.is_private
}
