# Проектная работа 9 спринта

https://github.com/dimkaddi/ugc_sprint_2

## Исследование

Обновлено описание [здесь](src/research/README.md)

## Работа с проектом

запуск MongoDB: 
    
    make run_environment

Запуск сервиса локально:

    run_ugc

Для запуска сервиса в проде (отключить проброс портов сервиса и запустить nginx):

    make run_prod

# Проектная работа 8 спринта

https://github.com/dimkaddi/ugc_sprint_1

Запуск окружения (кафка и кликхаус):

    make run_environment

Доступ к кавке: http://127.0.0.1:9021/

После поднятия окружения требуется установить зависимости для скрипта, который настроит etl:

    make prepare && make setup_etl

Тестовые данные для кафки можно сгенерировать командой:

    make gen_views

## Запуск сервиса для production

Для запуска сервиса в проде (отключить проброс портов сервиса и запустить nginx):

    make run_prod

Доступ к openapi сервиса ugc: http://127.0.0.1/api/openapi

## Исследование

Описание [здесь](src/research/README.md)