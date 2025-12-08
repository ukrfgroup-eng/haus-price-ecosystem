"""
Главное приложение MATRIX CORE API для экосистемы Дома-Цены.РФ
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Создаем приложение Flask
app = Flask(__name__)
CORS(app)

# Конфигурация
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///haus_price.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-this')

# Импортируем модели и инициализируем БД
from backend.models import db
db.init_app(app)

# ==================== РОТЫ API ====================

@app.route('/')
def home():
    """Главная страница API"""
    return jsonify({
        'status': 'online',
        'service': 'MATRIX CORE API - Дома-Цены.РФ',
        'version': '1.0.0',
        'description': 'Ядро экосистемы загородного строительства',
        'endpoints': {
            'health': '/health',
            'api_docs': '/api/v1/docs',
            'partners': '/api/v1/partners',
            'webhooks': {
                'protalk': '/webhook/protalk',
                'umnico': '/webhook/umnico',
                'tilda': '/webhook/tilda'
            }
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности системы"""
    try:
        # Проверка базы данных
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = 'disconnected'
    
    # Проверка API ФНС
    try:
        from backend.services.fns_service import fns_service
        fns_status = 'available' if fns_service.api_key else 'unavailable'
    except:
        fns_status = 'unavailable'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'components': {
            'database': db_status,
            'fns_api': fns_status,
            'api_server': 'running'
        }
    })


@app.route('/api/v1/partners/register', methods=['POST'])
def register_partner():
    """Регистрация нового партнера"""
    try:
        data = request.json
        logger.info(f"Регистрация партнера: {data.get('company_name')}")
        
        # Валидация обязательных полей
        required_fields = ['company_name', 'inn', 'contact_person', 'phone', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Не заполнено обязательное поле: {field}'
                }), 400
        
        # Проверка ИНН через API ФНС
        from backend.services.fns_service import fns_service
        inn_result = fns_service.check_inn(data['inn'])
        
        if not inn_result['success']:
            return jsonify({
                'success': False,
                'error': 'Ошибка верификации ИНН',
                'details': inn_result.get('error')
            }), 400
        
        # Проверяем, не зарегистрирован ли уже этот ИНН
        existing_partner = Partner.query.filter_by(inn=data['inn']).first()
        if existing_partner:
            return jsonify({
                'success': False,
                'error': 'Компания с таким ИНН уже зарегистрирована',
                'partner_code': existing_partner.partner_code
            }), 409
        
        # Создаем нового партнера
        partner = Partner(
            company_name=data['company_name'],
            legal_form=data.get('legal_form', 'ООО'),
            inn=data['inn'],
            contact_person=data['contact_person'],
            phone=data['phone'],
            email=data['email'],
            verification_data=inn_result.get('data'),
            verification_status='pending_documents',
            status='registration_in_progress',
            registration_stage='inn_verified'
        )
        
        # Генерируем код партнера
        from datetime import datetime
        partner.partner_code = f"P-{datetime.now().strftime('%y%m%d')}{Partner.query.count() + 1:04d}"
        
        db.session.add(partner)
        db.session.commit()
        
        logger.info(f"Партнер зарегистрирован: {partner.partner_code}")
        
        return jsonify({
            'success': True,
            'partner': partner.to_dict(),
            'message': 'Регистрация начата успешно',
            'next_steps': [
                {
                    'step': 'upload_documents',
                    'description': 'Загрузите документы компании в личном кабинете',
                    'url': f"{os.getenv('PARTNER_PORTAL_URL')}/upload/{partner.partner_code}"
                },
                {
                    'step': 'complete_profile',
                    'description': 'Заполните профиль услуг и специализаций',
                    'url': f"{os.getenv('PARTNER_PORTAL_URL')}/profile/{partner.partner_code}"
                }
            ]
        }), 201
        
    except Exception as e:
        logger.error(f"Ошибка регистрации партнера: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Внутренняя ошибка сервера',
            'details': str(e)
        }), 500


@app.route('/api/v1/partners/<partner_code>', methods=['GET'])
def get_partner(partner_code):
    """Получение информации о партнере по коду"""
    try:
        partner = Partner.query.filter_by(partner_code=partner_code).first()
        
        if not partner:
            return jsonify({
                'success': False,
                'error': 'Партнер не найден'
            }), 404
        
        return jsonify({
            'success': True,
            'partner': partner.to_dict(),
            'registration_progress': {
                'stage': partner.registration_stage,
                'status': partner.verification_status,
                'completed': partner.status == 'active'
            }
        })
        
    except Exception as e:
        logger.error(f"Ошибка получения партнера {partner_code}: {e}")
        return jsonify({
            'success': False,
            'error': 'Ошибка при получении данных'
        }), 500


@app.route('/webhook/protalk', methods=['POST'])
def handle_protalk_webhook():
    """Обработка вебхуков от Protalk бота"""
    try:
        data = request.json
        logger.info(f"Получен вебхук от Protalk: {data.get('type', 'unknown')}")
        
        # Проверка секретного ключа
        webhook_secret = request.headers.get('X-Webhook-Secret')
        expected_secret = os.getenv('PROTALK_WEBHOOK_SECRET')
        
        if webhook_secret != expected_secret:
            logger.warning(f"Неверный секретный ключ вебхука")
            return jsonify({'error': 'Invalid webhook secret'}), 401
        
        # Обработка разных типов событий
        event_type = data.get('type', 'message')
        
        if event_type == 'message':
            # Обработка сообщения от пользователя
            user_message = data.get('message', {}).get('text', '')
            user_id = data.get('user', {}).get('id')
            bot_id = data.get('bot', {}).get('id')
            
            # Здесь будет логика обработки сообщения
            response = process_bot_message(user_id, bot_id, user_message, data)
            
            return jsonify(response)
        
        elif event_type == 'command':
            # Обработка команды (например, /start)
            command = data.get('command')
            user_id = data.get('user', {}).get('id')
            
            if command == '/start':
                return jsonify({
                    'response': '🏢 Добро пожаловать в регистрацию партнера!',
                    'actions': [
                        {
                            'type': 'text',
                            'text': 'Для начала введите название вашей компании:'
                        }
                    ]
                })
        
        return jsonify({'status': 'received'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука Protalk: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/webhook/umnico', methods=['POST'])
def handle_umnico_webhook():
    """Обработка вебхуков от Umnico (чат на сайте)"""
    try:
        data = request.json
        logger.info(f"Получен вебхук от Umnico")
        
        # Определение типа пользователя
        message = data.get('message', '').lower()
        user_id = data.get('userId')
        
        response = {
            'messages': [],
            'actions': []
        }
        
        # Ключевые слова для определения партнера
        partner_keywords = ['партнер', 'компания', 'регистрация', 'сотрудничать', 'юрлицо', 'ип']
        
        if any(keyword in message for keyword in partner_keywords):
            # Пользователь - потенциальный партнер
            response['messages'].append({
                'text': '🏢 Отлично! Я вижу, вы хотите стать партнером нашей экосистемы.',
                'type': 'text'
            })
            response['messages'].append({
                'text': 'Для регистрации компании перейдите в нашего бота:',
                'type': 'text'
            })
            response['actions'].append({
                'type': 'button',
                'text': '📱 Перейти в бот регистрации',
                'url': 'https://t.me/partner_haus_price_bot'
            })
        else:
            # Пользователь - заказчик
            response['messages'].append({
                'text': '🔨 Привет! Я помогу вам найти исполнителя для вашего проекта.',
                'type': 'text'
            })
            response['messages'].append({
                'text': 'Расскажите, что вы хотите построить или отремонтировать?',
                'type': 'text'
            })
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука Umnico: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/webhook/tilda', methods=['POST'])
def handle_tilda_webhook():
    """Обработка вебхуков от Tilda (личный кабинет)"""
    try:
        data = request.json
        form_id = data.get('formid')
        partner_code = data.get('partner_code')
        
        logger.info(f"Получены данные из Tilda, форма: {form_id}, партнер: {partner_code}")
        
        if form_id == 'partner_registration_complete':
            # Завершение регистрации через личный кабинет
            partner = Partner.query.filter_by(partner_code=partner_code).first()
            
            if partner:
                partner.registration_stage = 'completed'
                partner.verification_status = 'pending_review'
                partner.status = 'awaiting_activation'
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Регистрация завершена успешно',
                    'partner_code': partner_code,
                    'next_steps': 'Ожидайте активации аккаунта в течение 24 часов'
                })
        
        return jsonify({'status': 'received'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука Tilda: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def process_bot_message(user_id, bot_id, message, context):
    """Обработка сообщений от ботов"""
    # Заглушка - будет реализована позже
    return {
        'response': f"Получено сообщение: {message}",
        'next_step': 'request_company_name',
        'user_id': user_id
    }


# Импорт для функции health_check
from datetime import datetime

# Создаем таблицы при запуске
with app.app_context():
    db.create_all()
    logger.info("База данных инициализирована")

# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Запуск MATRIX CORE API на порту {port}, debug: {debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
