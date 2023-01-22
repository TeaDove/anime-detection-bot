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
  lambda_fullname = join("-", [var.global_deployment_settings["name_prefix"], "container-model"])
  src_directory   = "${var.global_deployment_settings["src_path"]}/model_api"
  image_name      = "ml-image"
}

resource "yandex_serverless_container" "container" {
  name = local.lambda_fullname

  memory            = 512
  execution_timeout = "30s"
  cores             = 1
  core_fraction     = 5
  concurrency       = 0

  service_account_id = yandex_iam_service_account.sa.id
  image {
    url = "cr.yandex/${data.external.registry_id.result["id"]}/${local.image_name}:latest"
    environment = merge({
      "POWERTOOLS_SERVICE_NAME" : local.lambda_fullname
      "service_aws_access_key_id" : yandex_iam_service_account_static_access_key.sa_static_key.access_key,
      "service_aws_secret_access_key" : yandex_iam_service_account_static_access_key.sa_static_key.secret_key
    }, var.lambda_envs)
  }
}

resource "yandex_iam_service_account" "sa" {
  name = join("-", [var.global_deployment_settings["name_prefix"], "model-sa"])
}

resource "yandex_resourcemanager_folder_iam_binding" "sa_binding" {
  role      = each.value
  members   = ["serviceAccount:${yandex_iam_service_account.sa.id}"]
  folder_id = var.global_deployment_settings["yc_folder_id"]
  for_each = {
    "role1" : "storage.viewer",
    "role2" : "container-registry.images.puller",
    "role3" : "serverless.containers.invoker"
  }
}

resource "yandex_iam_service_account_static_access_key" "sa_static_key" {
  service_account_id = yandex_iam_service_account.sa.id
}
