from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from models import User


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
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
def ep1():
    return render_template('ep1.html')


@app.route('/ep2')
def ep2():
    return render_template('ep2.html')


@app.route('/ep3')
def ep3():
    return render_template('ep3.html')


@app.route('/login', methods=['POST', 'GET'])
def auth():
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
def register():
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
def secrettrack():
    """
    Защищенная страница, требующая аутентификации пользователя.
    """
    return render_template('secrettrack.html')


@app.route('/logout')
@login_required
def logout():
    """
    Функция выхода пользователя из аккаунта.
    """
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    """
    Перенаправление на страницу аутентификации в случае отсутствия авторизации
    """
    if response.status_code == 401:
        return redirect(url_for('auth'))
    return response
