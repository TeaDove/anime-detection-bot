### DO NOT CHANGE ###
locals {
  stage = get_env("STAGE", "stable")

  # В deploy_config.yaml хранятся настройки для конкретного стека, они овверайдят дефолтные настройки
  local_yaml_config      = yamldecode(file("deploy_config.yaml"))
  local_stage_config_pre = lookup(local.local_yaml_config["envs"], local.stage, {})
  local_defaults_pre     = lookup(local.local_yaml_config, "defaults", {})

  local_yaml_secrets     = yamldecode(file("secrets.yaml"))
  local_stage_secrets    = lookup(local.local_yaml_secrets["envs"], local.stage, {})
  local_secrets_defaults = lookup(local.local_yaml_secrets, "defaults", {})

  local_stage_config = merge(local.local_stage_config_pre, local.local_stage_secrets)
  local_defaults     = merge(local.local_defaults_pre, local.local_secrets_defaults)
  # Соединяем local, default и common конфиги по приоритету локальности Default -> LocalDefault -> Local.
  stage_vars = merge(local.local_defaults, local.local_stage_config)

  department         = local.local_yaml_config["department"]
  stack              = local.local_yaml_config["stack"]
  is_prod            = lookup(local.stage_vars, "is_prod", local.stage == "prod" ? true : false)
  terraform_dir_path = get_env("PWD", ".")
  src_path           = "${local.terraform_dir_path}/${local.local_yaml_config["src_path"]}"
  name_prefix        = lower(join("-", [title(local.stage), title(local.department), local.stack]))
  global_deployment_settings = {
    "stage" : local.stage
    "department" : local.department
    "stack" : local.stack
    "is_prod" : local.is_prod
    "terraform_dir_path" : local.terraform_dir_path
    "src_path" : local.src_path
    "name_prefix" : local.name_prefix
    "yc_cloud_id" : local.stage_vars["yc_cloud_id"]
    "yc_folder_id" : local.stage_vars["yc_folder_id"]
    "yc_zone" : local.stage_vars["yc_zone"]
  }
}

inputs = merge(local.stage_vars, { global_deployment_settings = local.global_deployment_settings }
)

// generate "provider" {
//   path      = "provider.tf"
//   if_exists = "overwrite_terragrunt"
//   contents  = <<EOF
// terraform {
//   required_providers {
//     telegram = {
//       source = "yi-jiayu/telegram"
//       version = "0.2.1"
//     }
//   }
// }

// provider "yandex" {
//   cloud_id  = "${local.stage_vars["yc_cloud_id"]}"
//   folder_id = "${local.stage_vars["yc_folder_id"]}"
//   zone      = "${local.stage_vars["yc_zone"]}"
// }

// // provider "telegram" {
// //   bot_token = "${local.stage_vars["bot_token"]}"
// // }
// EOF
// }

### DO NOT CHANGE ###
