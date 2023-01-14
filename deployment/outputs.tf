output "apigw_invoke_url" {
  value = "https://${module.apigw.apigw_id}.apigw.yandexcloud.net"
}
