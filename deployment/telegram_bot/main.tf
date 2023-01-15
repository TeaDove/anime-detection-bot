terraform {
  required_providers {
    telegram = {
      source  = "yi-jiayu/telegram"
      version = "0.3.1"
    }
  }
}

provider "telegram" {
  bot_token = var.bot_token
}

resource "telegram_bot_webhook" "webhook" {
  url             = "${var.api_gateway_invoke_url}/webhook"
  allowed_updates = ["message"]
}

resource "telegram_bot_commands" "commands" {
  commands = [
    {
      command     = "predict",
      description = "predict level of anime of image"
    },
    {
      command     = "help",
      description = "show help"
    }
  ]
}
