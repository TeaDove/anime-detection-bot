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

// Create SA
resource "yandex_iam_service_account" "sa" {
  folder_id = var.global_deployment_settings["yc_folder_id"]
  name      = join("-", [var.global_deployment_settings["name_prefix"], "wiegth-bucket-sa"])
}

// Grant permissions
resource "yandex_resourcemanager_folder_iam_member" "sa_editor" {
  folder_id = var.global_deployment_settings["yc_folder_id"]
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

// Create Static Access Keys
resource "yandex_iam_service_account_static_access_key" "sa_static_key" {
  service_account_id = yandex_iam_service_account.sa.id
}

// Use keys to create bucket
resource "yandex_storage_bucket" "bucket" {
  access_key = yandex_iam_service_account_static_access_key.sa_static_key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa_static_key.secret_key
  bucket     = join("-", [var.global_deployment_settings["name_prefix"], "wiegth-bucket"])
}
