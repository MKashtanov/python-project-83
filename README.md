### Hexlet tests and linter status:
[![Actions Status](https://github.com/MKashtanov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/MKashtanov/python-project-83/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/f44c665edaed2e74073d/maintainability)](https://codeclimate.com/github/MKashtanov/python-project-83/maintainability)

## Описание

[Page Analyzer](https://page-analyzer-lxc1.onrender.com "результат можно посмотреть здесь")  – это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с [PageSpeed Insights](https://pagespeed.web.dev/):

![Изображение](img/index.png "Внешний вид главной страницы")

![Изображение](img/sites.png "Список опрошенных сайтов")

![Изображение](img/site.png "Свойства сайта и даты проверок")

## Зависимости

* python >= 3.10
* poetry >= 1.6
* PostgreSQL >= 15.4

## Запуск приложения

Клонируем репозиторий ```git clone https://github.com/MKashtanov/python-project-83.git```

Запускаем установку зависимостей ```make install```

Для работы приложения нужны две переменные окружения ```$DATABASE_URL``` и ```$SECRET_KEY```.

Вы можете создать .env файл внутри проекта для установки значений этих переменных, либо задать их любым другим способом.

```
DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{db}'
# postgresql://janedoe:mypassword@localhost:5432/mydb
SECRET_KEY = 'I AM THE SECRET'
```

Запускаем приложение ```make start```

Для автоматического деплоя есть файл ```build.sh``` который нужно будет указать на сервисе деплоя.