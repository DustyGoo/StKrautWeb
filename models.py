"""
Модуль проекта StKrautWeb для взаимосвязи базы данных и приложения.
"""

from flask_login import UserMixin

from app import app, db, manager


class User(db.Model, UserMixin):
    """
    Модель пользователя для хранения информации о пользователях в базе данных.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        login (str): Логин пользователя, уникальное поле.
        password (str): Хэшированный пароль пользователя.
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(48))


# Создаем все таблицы базы данных, если они еще не существуют
with app.app_context():
    db.create_all()


@manager.user_loader
def load_user(user_id: int) -> User:
    """
    Функция для загрузки пользователя из базы данных по его идентификатору.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        User: Объект пользователя, соответствующий переданному идентификатору,
              или None, если пользователь не найден.
    """
    return User.query.get(user_id)
