"""
Модуль для конфигурации проекта, создания основных объектов расширений (db,
        manager и остальные, которые есть)

Этот модуль отвечает за инициализацию основного объекта Flask приложения,
его конфигурацию,а также подключение и настройку различных расширений Flask.
Включает в себя настройку подключения к базе данных, отображение
всплывающих уведомлений и инструменты для отладки.
"""

import uuid

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr


# Создание экземпляра Flask-приложения
app = Flask(__name__)

# Настройка URI для подключения к базе данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Генерация случайного ключа для безопасности сессий
app.config['SECRET_KEY'] = str(uuid.uuid4())

# Установка таймаута для уведомлений Toastr в миллисекундах
app.config['TOASTR_TIMEOUT'] = 2000

# Создаем объект SQLAlchemy для работы с базой данных
db = SQLAlchemy(app)

# Создаем объект Manager для управления командами Flask
manager = LoginManager(app)

# Создание объекта Toastr для отображения уведомлений в приложении
toastr = Toastr(app)
