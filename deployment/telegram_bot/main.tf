resource "null_resource" "set_weebhook" {
  triggers = {
    everytime = uuid()
  }

  provisioner "local-exec" {
    command = "curl --request POST --url https://api.telegram.org/bot${var.bot_token}/setWebhook --header 'content-type: application/json' --data '{\"url\": \"${var.api_gateway_invoke_url}/webhook\"}'"
  }

  # provisioner "local-exec" {
  #   when    = destroy
  #   command = "curl --request POST --url https://api.telegram.org/bot${var.bot_token}/removeWebhook"
  # }
}
