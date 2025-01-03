# Используем официальный образ Python
FROM python:3.9-slim

# Установим рабочую директорию
WORKDIR /app

# Скопируем зависимости
COPY requirements.txt requirements.txt

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем проект в контейнер
COPY . .

# Укажем порт, на котором будет работать приложение
EXPOSE 8000

# Команда запуска Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "chelli.wsgi:application"]