-- База данных для партнеров экосистемы Дома-Цены.РФ

CREATE TABLE partners (
    id SERIAL PRIMARY KEY,
    partner_code VARCHAR(20) UNIQUE NOT NULL,  -- P-000001
    status VARCHAR(20) DEFAULT 'pending',      -- pending, verified, active, suspended
    
    -- Основные данные
    company_name VARCHAR(255) NOT NULL,
    legal_form VARCHAR(10) NOT NULL,           -- ООО, ИП, АО
    inn VARCHAR(12) UNIQUE NOT NULL,
    ogrn VARCHAR(15),
    registration_date DATE,
    
    -- Контактные данные
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    website VARCHAR(255),
    
    -- Юридический адрес
    legal_address TEXT,
    actual_address TEXT,
    
    -- Услуги и специализация
    main_category VARCHAR(50),                 -- contractor, manufacturer, seller, executor
    specializations JSONB,                     -- ["каркасные дома", "отделка"]
    regions JSONB,                             -- ["Москва", "Московская область"]
    
    -- Верификация
    verification_status VARCHAR(20) DEFAULT 'pending',
    verification_date TIMESTAMP,
    verification_method VARCHAR(50),           -- fns_api, kontur, manual
    verification_data JSONB,                   -- Ответ от API
    
    -- Документы
    documents JSONB,                           -- {ogrn_scan: "url", inn_scan: "url"}
    
    -- Настройки
    is_active BOOLEAN DEFAULT TRUE,
    subscription_plan VARCHAR(20) DEFAULT 'trial',
    subscription_expires DATE,
    
    -- Технические поля
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    telegram_user_id BIGINT,
    registration_source VARCHAR(50),           -- bot, website, personal_cabinet
    
    -- Индексы
    INDEX idx_partners_status (status),
    INDEX idx_partners_inn (inn),
    INDEX idx_partners_telegram_id (telegram_user_id),
    INDEX idx_partners_regions (regions)
);

-- Таблица истории регистрации
CREATE TABLE registration_logs (
    id SERIAL PRIMARY KEY,
    partner_id INTEGER REFERENCES partners(id),
    step VARCHAR(50),                          -- company_name, inn_verification, etc
    action VARCHAR(50),                        -- started, completed, failed
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица верификационных запросов
CREATE TABLE verification_requests (
    id SERIAL PRIMARY KEY,
    partner_id INTEGER REFERENCES partners(id),
    inn VARCHAR(12),
    api_provider VARCHAR(50),                  -- fns, kontur
    request_data JSONB,
    response_data JSONB,
    status VARCHAR(20),                        -- success, error, pending
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
