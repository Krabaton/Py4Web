# Docker-команда FROM указывает базовый образ контейнера
# Наш базовый образ - это Linux с предустановленным python-3.7
FROM python:3.9
# gettext-base нужен для того, чтобы установить envsubst
RUN apt update
# Скопируем файл с зависимостями в контейнер
COPY Pipfile .
COPY Pipfile.lock .
# Установим зависимости внутри контейнера
RUN pip install pipenv \
    && pipenv lock --keep-outdated --requirements > requirements.txt \
    && pip install -r requirements.txt
# Скопируем остальные файлы в контейнер
COPY . .
# разрешаем наш скрипт на исполнение операционной системой
RUN chmod +x run.sh
# запускаем скрипт
CMD ["./run.sh"]