terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  cloud_id  = var.global_deployment_settings["yc_cloud_id"]
  folder_id = var.global_deployment_settings["yc_folder_id"]
  zone      = var.global_deployment_settings["yc_zone"]
}

locals {
  lambda_name     = "bot-api"
  src_directory   = "${var.global_deployment_settings["src_path"]}/bot_api"
  lambda_fullname = join("-", [var.global_deployment_settings["name_prefix"], local.lambda_name])
}


resource "null_resource" "compile_requirements" {
  triggers = {
    redeploy = uuid()
  }
  provisioner "local-exec" {
    command = "cd ${local.src_directory} && ./compile_requirements.sh"
  }
}

data "archive_file" "archive" {
  type        = "zip"
  source_dir  = local.src_directory
  output_path = "${local.src_directory}/.deploy.zip"
  excludes    = ["${local.src_directory}/.deploy.zip"]

  depends_on = [null_resource.compile_requirements]
}

resource "yandex_function" "function" {
  name               = local.lambda_fullname
  user_hash          = data.archive_file.archive.output_base64sha256
  runtime            = "python311"
  entrypoint         = "entrypoints.handler"
  memory             = "512"
  execution_timeout  = "5"
  service_account_id = yandex_iam_service_account.sa.id

  content {
    zip_filename = data.archive_file.archive.output_path
  }

  environment = merge({
    POWERTOOLS_SERVICE_NAME = local.lambda_fullname
    security_yc_access_key  = yandex_iam_service_account_static_access_key.sa_static_key.access_key
    security_yc_secret_key  = yandex_iam_service_account_static_access_key.sa_static_key.secret_key
  }, var.lambda_envs)
}

resource "yandex_iam_service_account" "sa" {
  name = join("-", [var.global_deployment_settings["name_prefix"], "sa"])
}

resource "yandex_resourcemanager_folder_iam_binding" "sa_binding" {
  role      = each.value
  members   = ["serviceAccount:${yandex_iam_service_account.sa.id}"]
  folder_id = var.global_deployment_settings["yc_folder_id"]
  for_each = {
    "role1" : "serverless.functions.invoker"
    "role2" : "serverless.containers.invoker"
  }
}

resource "yandex_iam_service_account_static_access_key" "sa_static_key" {
  service_account_id = yandex_iam_service_account.sa.id
}
