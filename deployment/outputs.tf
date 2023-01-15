output "api_gateway_invoke_url" {
  value = local.api_gateway_invoke_url
}

output "container_invoke_url" {
  value = "https://${module.container_model.container_id}.containers.yandexcloud.net"
}
