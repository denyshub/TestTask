# Використовуємо базовий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл з залежностями
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код у контейнер
COPY . .

# Виконати міграції та зібрати статичні файли
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Вказуємо команду для запуску сервера
CMD ["gunicorn", "my_django_app.wsgi:application", "--bind", "0.0.0.0:8000"]

# Відкриваємо порт для зовнішнього доступу
EXPOSE 8000
