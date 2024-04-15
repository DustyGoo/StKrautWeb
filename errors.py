from flask import render_template

from app import app


@app.errorhandler(404)
def error404(error: Exception) -> tuple:
    """
    Обрабатывает ошибку 404.

    Args:
        error (Exception): Объект исключения.

    Returns:
        tuple: Кортеж с шаблоном страницы ошибки и кодом ошибки 404.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def error404(error: Exception) -> tuple:
    """
    Обрабатывает ошибку 500.

    Args:
        error (Exception): Объект исключения.

    Returns:
        tuple: Кортеж с шаблоном страницы ошибки и кодом ошибки 500.
    """
    return render_template('500.html'), 500
