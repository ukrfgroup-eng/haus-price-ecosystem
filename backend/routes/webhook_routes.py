"""
Маршруты для вебхуков
"""

from flask import Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/umniko', methods=['POST'])
def umniko_webhook():
    """Обработка вебхука от ProTalk"""
    data = request.get_json()
    return jsonify({"status": "success", "message": "Webhook processed"})

@webhook_bp.route('/tilda', methods=['POST'])
def tilda_webhook():
    """Обработка вебхука от Tilda"""
    return jsonify({"status": "success"})

@webhook_bp.route('/flexbe', methods=['POST'])  
def flexbe_webhook():
    """Обработка вебхука от Flexbe"""
    return jsonify({"status": "success"})
