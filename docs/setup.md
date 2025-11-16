# Установка и настройка MATRIX CORE

## Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/doma-ceny/matrix-core-ecosystem.git
cd matrix-core-ecosystem
2. Настройка виртуального окружения
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Настройка переменных окружения
bash
cp .env.example .env
# Отредактируйте .env файл под ваши настройки
5. Запуск приложения
bash
python backend/app.py
Docker запуск
Сборка и запуск
bash
docker-compose up -d --build
Просмотр логов
bash
docker-compose logs -f web
Остановка
bash
docker-compose down
Настройка интеграций
Umniko бот
Создайте бота в Umniko

Настройте вебхук на: https://your-domain.com/api/v1/webhook/umniko

Добавьте API ключ в .env файл

Tilda
Настройте API доступ в Tilda

Добавьте API ключ в .env файл

Настройте вебхуки для синхронизации данных

Первоначальная настройка
Запустите приложение

Проверьте API endpoints через документацию

Настройте интеграции с внешними сервисами

Добавьте тестовых пользователей для проверки функционала

Тестирование
bash
# Запуск тестов
python -m pytest tests/

# Проверка здоровья API
curl http://localhost:5000/api/v1/health
Приложение будет доступно по адресу: http://localhost:5000
