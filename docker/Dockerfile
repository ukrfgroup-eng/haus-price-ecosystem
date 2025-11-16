FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY backend/ ./backend/

# Создаем папку для данных
RUN mkdir -p data

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "backend/app.py"]
