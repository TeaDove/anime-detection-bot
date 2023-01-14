terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

module "lambda_bot" {
  source = "./lambda_bot"

  lambda_envs = { "LOG_LEVEL" : var.log_level }

  global_deployment_settings = var.global_deployment_settings
}

module "apigw" {
  source = "./apigw"

  function_id                 = module.lambda_bot.function_id
  function_service_account_id = module.lambda_bot.service_account_id

  global_deployment_settings = var.global_deployment_settings
}
