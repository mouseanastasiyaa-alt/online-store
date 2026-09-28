# Online Store 

Учебный проект интернет-магазина на Django, разрабатываемый в рамках курса.

## Описание

Проект представляет собой интернет-магазин плагинов и примеров кода (Skystore).
На текущем этапе реализованы базовые страницы: главная (каталог) и контакты.

## Стек

- Python 3.14
- Django 6.1.1
- Bootstrap 5 (CDN)
- SQLite (по умолчанию)

## Установка и запуск

1. Клонировать репозиторий:

   git clone https://github.com/mouseanastasiyaa-alt/online-store.git
   cd online-store

2. Создать и активировать виртуальное окружение:

   python -m venv venv
   .venv\Scripts\activate    # Windows

3. Установить зависимости: 
   
   pip install -r requirements.txt

4. Применить миграции:

   python manage.py migrate

5. Запустить сервер:

   python manage.py runserver
6. Открыть в браузере:

   http://127.0.0.1:8000/

Структура проекта

online-store/
├── config/          # Настройки Django
├── catalog/         # Приложение каталога
├── manage.py
├── requirements.txt
└── .gitignore

Ветки
main — стабильная версия

develop — ветка разработки

feature/* — ветки под отдельные задачи

Автор
Анастасия (@mouseanastasiyaa-alt)



