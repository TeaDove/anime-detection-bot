variable "bot_token" { sensitive = true }
variable "lambda_envs" { type = map(string) }
variable "container_envs" { type = map(string) }
variable "rebuild_image" { type = bool }

### DO NOT CHANGE ###
variable "global_deployment_settings" { type = map(string) }
### DO NOT CHANGE ###
