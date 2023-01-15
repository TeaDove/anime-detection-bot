### Установка
- Скачать [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) и [terragrunt](https://terragrunt.gruntwork.io/docs/getting-started/install/) (заходить из под ВПН)
### Команды
```shell
STAGE=stable terragrunt init -reconfigure # Инициализация, надо сделать 1 раз при смене стека

STAGE=stable terragrunt plan  # Планирование стека на стенд "stable"
STAGE=stable terragrunt apply # Выполнение стека на стенд "stable"
```
### Yandex Cloud
```shell
export YC_TOKEN=(yc iam create-token)

### Настройка
- Настройка стейджа и региона деплоймента ведется в `deploy_config.yaml`
- Настройка инфраструктуры ведется в файлах `*.tf`

### Container
```shel
curl --location --request POST 'https://bbapbfnrn3n0ep31v3pr.containers.yandexcloud.net/predict' \
  --header "Authorization: Bearer $(yc iam create-token)" \
  --form 'image=@"../service/model_api/tests/images/0a0.png'
```
