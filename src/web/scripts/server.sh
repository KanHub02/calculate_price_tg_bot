#!/bin/sh
echo "Создаю миграции..."
python manage.py makemigrations
echo "Отправляю миграции..."
python manage.py migrate
echo "Собираю статику..."
python manage.py collectstatic --no-input
echo "Запускаю сервер..."
python3 manage.py runserver 0.0.0.0:8811
