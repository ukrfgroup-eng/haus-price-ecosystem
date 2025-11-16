# 🏗️ Структура проекта ДОМА-ЦЕНЫ.РФ

## 🌟 Общая архитектура MATRIX CORE
🚀 ДОМА-ЦЕНЫ.РФ - Нейро-экосистема строительства
├── 🧠 MATRIX CORE (Центральный AI-мозг)
│ ├── 🤖 Neural Orchestrator
│ ├── 🔄 Когнитивный протокол обмена
│ └── 🎯 Эмерджентный интеллект
├── 🌐 Интерфейсный слой
│ ├── 💬 Protalk/Umniko боты
│ ├── 🎨 Flexbe (Главная страница)
│ └── 👤 Tilda (Личный кабинет)
└── 📊 Специализированные модули
├── 🤝 AI-Партнер
├── 🔍 AI-Подбор
└── 💡 AI-Рекомендации

text

## 📁 Файловая структура репозитория
doma-ceny-rf/
├── 🎯 ОСНОВНЫЕ ФАЙЛЫ
│ ├── README.md # 📖 Главное описание проекта
│ ├── PROJECT-STRUCTURE.md # 🗺️ Этот файл - карта проекта
│ ├── .gitignore # 🚫 Игнорируемые файлы
│ ├── requirements.txt # 🐍 Зависимости Python
│ ├── docker-compose.yml # 🐳 Docker компоновка
│ └── .env.example # ⚙️ Пример переменных окружения
│
├── 🧠 BACKEND (MATRIX CORE)
│ ├── init.py # 📦 Пакет backend
│ ├── app.py # 🚀 Основное приложение Flask
│ ├── config.py # ⚙️ Конфигурация приложения
│ │
│ ├── 🗃️ models/ # 💾 Модели данных
│ │ ├── init.py
│ │ ├── user_models.py # 👥 Модели пользователей
│ │ ├── partner_models.py # 🤝 Модели партнеров
│ │ └── analysis_models.py # 📊 Модели анализа
│ │
│ ├── 🛣️ routes/ # 🌐 API Маршруты
│ │ ├── init.py
│ │ ├── analysis_routes.py # 🧮 Аналитические endpoint-ы
│ │ ├── partner_routes.py # 🤝 Партнерские endpoint-ы
│ │ ├── user_routes.py # 👥 Пользовательские endpoint-ы
│ │ └── connection_routes.py # 🔗 Endpoint-ы соединений
│ │
│ └── 🛠️ utils/ # 🔧 Утилиты и хелперы
│ ├── init.py
│ ├── ai_helpers.py # 🤖 AI-помощники
│ ├── data_helpers.py # 💾 Хелперы данных
│ └── webhook_helpers.py # 🌐 Вебхук-обработчики
│
├── 🎨 FRONTEND # 🖥️ Фронтенд интеграции
│ ├── flexbe/ # ⚡ Главная страница
│ │ └── (интеграционные файлы)
│ ├── tilda/ # 👤 Личный кабинет
│ │ └── (интеграционные файлы)
│ └── umniko/ # 🤖 Боты-коммуникаторы
│ └── (сценарии ботов)
│
├── 📚 DOCS # 📖 Документация
│ ├── api.md # 🌐 Документация API
│ ├── setup.md # ⚙️ Инструкция по установке
│ └── whitepaper.md # 💼 White paper для инвесторов
│
├── 🐳 DOCKER # 🐳 Контейнеризация
│ └── Dockerfile # 🏗️ Образ Docker
│
└── 🧪 TESTS # ✅ Тестирование
├── init.py
├── test_models.py # 🧪 Тесты моделей
├── test_routes.py # 🧪 Тесты API
└── test_utils.py # 🧪 Тесты утилит

text

## 🔄 Взаимодействие компонентов

### Поток данных:
Пользователь → [Umniko бот] → [Gateway API] → [MATRIX CORE] → [Спец. модули]
↓
Ответ ← [Бот] ← [Форматирование] ← [AI-обработка] ← [База данных]

text

### Технологический стек:
- **Backend**: Python/Flask, SQLite/PostgreSQL
- **Frontend**: Flexbe, Tilda, Umniko боты  
- **Infrastructure**: Docker, Nginx, GitHub Actions
- **AI/ML**: Интеллектуальные алгоритмы подбора и рекомендаций

## 🎯 Ключевые особенности архитектуры

### 🧠 MATRIX CORE принципы:
1. **Децентрализованный интеллект** - каждый модуль автономен
2. **Нейропластичность** - система адаптируется к изменениям
3. **Эмерджентное поведение** - сложные паттерны из простых правил
4. **Коллективное обучение** - опыт одного улучшает всех

### 🔄 Протоколы взаимодействия:
- **REST API** для внешних интеграций
- **Webhook** для реального времени
- **Внутренняя шина** для межмодульного общения
- **Когнитивный обмен** для передачи смыслов

---

## 📞 Для разработчиков

**Быстрый старт:**
```bash
git clone https://github.com/doma-ceny/matrix-core-ecosystem.git
cd matrix-core-ecosystem
docker-compose up -d
Документация:

API Documentation

Setup Guide

White Paper
