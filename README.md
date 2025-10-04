# 💰 Учет Движения Денежных Средств (ДДС) - Django Web Application

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17+-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-yellow)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1-purple)

## 📋 О проекте

**ДДС (движение денежных средств)** — это веб-приложение для учета, управления и анализа поступлений и списаний 
денежных средств компании или частного лица.

### 🚀 Ключевые возможности

**Основной функционал:**
- ✅ Полный CRUD для записей движения денежных средств
- ✅ Управление справочниками: категории, подкатегории, статусы, типы операций
- ✅ Расширяемые справочники с логическими зависимостями
- ✅ Фильтрация и поиск записей по различным параметрам
- ✅ Интуитивный интерфейс на Bootstrap 5
- ✅ Валидация данных на клиенте и сервере

**Мультипользовательская версия (feature_02):**
- 🔐 Индивидуальные пространства для каждого пользователя
- 👥 Пользователи видят только свои данные
- 🛡️ Безопасное разделение доступа

### 🧩 Основные модули

| Приложение   | Функционал                                                                       |
|--------------|----------------------------------------------------------------------------------|
| `cash_flow`  | Основной функционал: записи ДДС, категории, подкатегории, статусы, типы операций |
| `users`      | Управление пользователями: регистрация, вход                                     |

## 🏗 Структура проекта
``` 
Cash_Flow/
├── config/               # Django main settings
├── cash_flow/            # Main application
      └── templates/      # HTML templates
            └── base.html
        └── cashflow/
├── users/                # User management app
├── .env.example          # Environment example
├── pyproject.toml        # Poetry configuration
├── README.md             # Documentation
└── manage.py             # Entry point
``` 

## Приложение `users`
### 📦 Основные модели

```python
class User(AbstractUser):
    # Доп. поля:
    phone_number = models.CharField()  # Телефон
    avatar = models.ImageField()       # Фото профиля
    # ... и другие поля
```
## 🏥 Приложение cash_flow

Ядро системы с полным функционалом веб-приложения для регистрации движения денежных средств. Реализовано как 
отдельное Django-приложение с расширенной бизнес-логикой.

### 🧩 Основные модели

#### Модели данных

| Модель          | Описание                                       | Особенности                                                                                                           |
|-----------------|------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `Status`        | Модель статусов (Бизнес, Личное, Налог и др.)  | В версии (ветке) feature_01 приложение реализовано как отдельный самостоятельный сигемт, без привязки к пользователям |
| `OperationType` | Модель типов операций (Пополнение, Списание)   | В версии (ветке) feature_02 осуществлена приязка моделей к модели пользователя Users                                  |
| `Category `     | Категории операций (привязаны к типам)         |                                                                                                                       |
| `Subcategory `  | Подкатегории операций (привязаны к категориям) |                                                                                                                       |
| `CashFlow`      | Записи движения денежных средств               |                                                                                                                       |


## 🚀 Установка и запуск

### Предварительные требования
- Python 3.12+
- PostgreSQL 17+
- Poetry 

## 🎯 Версии проекта

**Клонирование репозитория:**

### 🌟 Feature 01 - Базовая версия
- **Одиночный пользователь**
- **Общие справочники**
- **Идеально для личного использования**

🔗 **[Код версии](https://github.com/HelenChern813/Cash_Flow/tree/feature_01)**

### 👥 Feature 02 - Мультипользовательская версия  
- **Индивидуальные пространства**
- **Изоляция данных между пользователями**
- **Идеально для компаний**

🔗 **[Код версии](https://github.com/HellenChern813/Cash_Flow/tree/feature_02)**

В основной ветку (main) - Объединено с веткой feature_01

**базовая команда для клонирования**
   ```bash
   git clone https://github.com/HelenChern813/Cash_Flow.git 
   cd Cash_Flow
```
**выбор версии (опционально)**
   ```bash
# Для базовой версии
git checkout feature_01
```
```bash
# Для мультипользовательской версии  
git checkout feature_02
```
**Активируйте виртуальное окружение и установите зависимости:**
   ```bash
poetry shell
poetry update
```
**Создайте файл .env с нужными конфигурациями для проекта по шаблону .env.example**
```
# Core settings
SECRET_KEY=your-secret-key
DEBUG=True

# Database
POSTGRES_DB=medical_db
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
- Если всё же нужна более "легкая" БД, то на файле settings.py измените настройки БД
- Для SQLite:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
**Применение миграций:**
   ```bash
python manage.py migrate
```

**Создание суперпользователя:**
   ```bash
python manage.py csu  
```
**Если нужны фикстуры для заполнения БД:**
- Для ветки feature_01:
```bash
python manage.py migrate && python manage.py loaddata cash_flow_fixture.json
python manage.py migrate && python manage.py loaddata users_fixture.json
```

- Для ветки feature_02:
```bash
python manage.py migrate && python manage.py loaddata cash_flow_fixture_2.json
python manage.py migrate && python manage.py loaddata users_fixture_2.json
```

**Запуск сервера:**
```bash
python manage.py runserver
```

### База данных
- PostgreSQL - основное хранилище данных

- psycopg2 - адаптер для работы с PostgreSQL

# 🎨 Интерфейс
## Основные страницы 

| Страница         | Назначение                                         |
|------------------|----------------------------------------------------|
| Главная          | Список записей ДДС с фильтрацией                   |
| Новая запись     | Форма создания записи движения средств             |
| Справочники      | Управление категориями, статусами, типами операций |
| Регистрация/Вход | Аутентификация пользователей                       |
| Добавить         | Форма создания новых объектов                      |    

## 📱 Особенности интерфейса
- Backend
- - Django 5.2 - основной фреймворк

- - Django ORM - работа с базой данных

- - Django Forms - валидация и обработка данных

- - Django Authentication - система аутентификации

- Frontend
- - Bootstrap 5 - UI фреймворк

- - JavaScript/jQuery - динамические элементы
