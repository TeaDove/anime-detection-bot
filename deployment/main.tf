locals {
  api_gateway_invoke_url = "https://${module.apigw.apigw_id}.apigw.yandexcloud.net"
}

module "storage_bucket" {
  source = "./storage_bucket"

  global_deployment_settings = var.global_deployment_settings
}

module "lambda_bot" {
  source = "./lambda_bot"

  lambda_envs = merge(var.lambda_envs, { "service_bot_token" : var.bot_token })

  global_deployment_settings = var.global_deployment_settings
}

module "container_model" {
  source = "./container_model"

  lambda_envs = merge(var.container_envs, {})

  global_deployment_settings = var.global_deployment_settings
}

module "apigw" {
  source = "./apigw"

  function_id                 = module.lambda_bot.function_id
  function_service_account_id = module.lambda_bot.service_account_id

  global_deployment_settings = var.global_deployment_settings
}

module "telegram_bot" {
  source = "./telegram_bot"

  api_gateway_invoke_url = local.api_gateway_invoke_url
  bot_token              = var.bot_token
}
