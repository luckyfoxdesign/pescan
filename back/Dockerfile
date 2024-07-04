# Используем официальный образ Python 3.9
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в текущую директорию в контейнере
COPY requirements.txt .

# Устанавливаем зависимости из файла
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

ENV FLASK_APP=app.py

# DEVELOPMENT
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

# PRODUCTION
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]