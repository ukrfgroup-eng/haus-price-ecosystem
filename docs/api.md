# MATRIX CORE API Documentation

## Базовые endpoint-ы

### Анализ пользовательского запроса
```http
POST /api/v1/analyze/request
Content-Type: application/json

{
  "user_type": "customer|contractor|producer",
  "message": "текст запроса",
  "user_data": {
    "region": "Московская область",
    "specialization": "каркасные дома",
    "budget_range": "1-3 млн",
    "timeline": "3 месяца"
  }
}
Поиск партнеров
http
POST /api/v1/partners/search
Content-Type: application/json

{
  "criteria": {
    "region": "Московская область",
    "specialization": "каркасные дома",
    "budget_range": "1-3 млн"
  }
}
Установление связи
http
POST /api/v1/connect/users
Content-Type: application/json

{
  "from_user": "user_id",
  "to_user": "partner_id",
  "context": "контекст запроса"
}
Коды ответов
200 Успешный запрос

400 Ошибка в данных запроса

500 Внутренняя ошибка сервера
