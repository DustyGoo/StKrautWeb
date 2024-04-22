"""
Модуль запуска проекта StKrautWeb
"""

if __name__ == '__main__':
    from controller import app
    from errors import app
    app.run(port=5010)
