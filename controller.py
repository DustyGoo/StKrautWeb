"""
Модуль Controller для проекта StKrautWeb.

Этот модуль содержит функции, которые обрабатывают запросы от пользователя.
Файл взаимодействует с моделями для получения данных и передает эти данные в
шаблоны для авторизации и отображения пользователям.
Каждое представление ассоциировано с URL-адресами.

Функции:
- index(): Главная страница приложения.
- ep1(), ep2(), ep3(): Страницы-визитки для отдельных альбомов
- register(): Регистрирует нового пользователя в системе.
- auth(): Авторизует пользователя в системе.
- secrettrack(): Позволяет пользователю просматривать закрытую страницу.
- logout(): Выполняет выход пользователя из системы.
- redirect_to_sign(): Перенаправляет неавторизованных пользователей на
страницу входа.
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from models import User


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index() -> Response | str:
    """
    Главная страница сайта.

    Возвращает или HTML-страницу, если запрос осуществляется методом GET
    или переводит пользователя на главную страницу после обработки данных
    формы, если запрос осуществляется методом POST.
    """
    if request.method == 'GET':
        return render_template('index.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
    return render_template('index.html')


# Функции ep1, ep2, ep3 - отвечают за отдельные тупиковые страницы сайта
@app.route('/ep1')
def ep1() -> Response | str:
    return render_template('ep1.html')


@app.route('/ep2')
def ep2() -> Response | str:
    return render_template('ep2.html')


@app.route('/ep3')
def ep3() -> Response | str:
    return render_template('ep3.html')


@app.route('/login', methods=['POST', 'GET'])
def auth() -> Response | str:
    """
    Авторизация пользователя.

    Возвращает или HTML-страницу, если запрос осуществляется методом GET
    или переводит пользователя на главную страницу после обработки данных
    формы, если запрос осуществляется методом POST.
    """
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=login).first()
    if user and not check_password_hash(user.password, password):
        flash({'title': "Статус", 'message': "Неверные данные!"},
              'error')
        return redirect(url_for('auth'))
    login_user(user)
    flash({'title': "Статус", 'message': "Успешная авторизация"},
          'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register() -> Response | str:
    """
    Регистрация пользователя.

    После зполнения форм переводит пользователя на главную страницу сайта
    """
    if request.method == 'GET':
        return render_template('register.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if not (3 < len(login) < 32 and 3 < len(password) < 32):
        return redirect(url_for('register'))
    password = generate_password_hash(password)
    user = User(login=login, password=password)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route('/secrettrack')
@login_required
def secrettrack() -> Response | str:
    """
    Защищенная страница, требующая аутентификации пользователя.
    """
    return render_template('secrettrack.html')


@app.route('/logout')
@login_required
def logout() -> Response | str:
    """
    Функция выхода пользователя из аккаунта.
    """
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    """
    Перенаправление на страницу аутентификации в случае отсутствия авторизации

    Эта функция вызывается автоматически после каждого запроса. Она проверяет
    статусный код ответа. Если статусный код ответа равен 401 (Неавторизован),
    происходит перенаправление пользователя на страницу регистрации и
    авторизации. Это обеспечивает, что пользователи, пытающиеся получить
    доступ к защищенным ресурсам без соответствующих прав доступа, будут
    направлены к форме входа, вместо отображения стандартной страницы с
    ошибкой 401.

    :param response: Объект ответа Flask, который был
    сгенерирован обработчиками запросов.
    :return: Исходный объект ответа или объект
    перенаправления на страницу авторизации.
    """
    if response.status_code == 401:
        return redirect(url_for('auth'))
    return response
