FROM python:3.12-slim

# Установим рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое папки task в /app/task
COPY task /app/task

# Устанавливаем рабочую директорию как /app
WORKDIR /app

# Запускаем main.py как модуль
CMD ["python", "-m", "task.main"]

