# All-In-One-Telegram-Bot

Telegram-бот с функционалом погоды и системой вебхуков, построенный на aiogram 3.x с использованием Pydantic, SQLAlchemy, Docker, PosgreSQL, Redis и др.

## Описание

Многофункциональный Telegram-бот, реализующий следующие возможности:

-   **Погода**: Агрегация данных о погоде из нескольких источников (OpenMeteo, WeatherAPI, VisualCrossing, Яндекс.Погода)
-   **Вебхуки**: Работа через webhook с использованием Tuna туннелей
-   **База данных**: SQLAlchemy ORM с поддержкой SQLite и PostgreSQL
-   **Кэширование**: Redis для оптимизации запросов
-   **Интернационализация**: Fluentogram для поддержки нескольких языков
-   **Логирование**: Структурированное логирование в JSON и консоль

## Архитектура

### Основные компоненты

```
bot/
├── src/
│   ├── core/              # Логирование
│   ├── database/          # Модели и репозитории
│   ├── handlers/          # Обработчики команд и callback
│   ├── keyboards/         # Клавиатуры (inline/reply)
│   ├── middlewares/       # Middleware (переводы, БД)
│   ├── services/          # Бизнес-логика (погода, геокодинг)
│   ├── states/            # FSM состояния
│   ├── filters/           # Callback фильтры
│   ├── i18n/              # Файлы переводов (Fluent)
│   └── utils/             # Утилиты (конфиг, парсинг, headers)
└── main.py                # Точка входа
```

### Паттерны проектирования

-   **Repository Pattern**: Абстракция работы с БД
-   **Factory Pattern**: Создание репозиториев и заголовков
-   **Middleware Pattern**: Обработка переводов и инъекция зависимостей
-   **FSM Pattern**: Управление состояниями диалога

## Требования

-   Python 3.10+
-   Docker и Docker Compose
-   Redis
-   Tuna CLI (для webhook туннелей)
-   Библиотеки python которые указаны в requirements.txt

## Установка

### Локальная установка

1. Клонируйте репозиторий:

```bash
git clone <repository-url>
cd All-In-One-Telegram-Bot
```

2. Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установите зависимости:

```bash
pip install -r bot/requirements.txt
```

4. Создайте файл `.env` в корне проекта:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_WEBHOOK_SECRET=your_webhook_secret

# Tuna Tunnels
TUNA_TOKEN=your_tuna_token
TUNA_API_TOKEN=your_tuna_api_token

# Database
DATABASE_STATUS=development  # или product
SQLITE_DB_URL=sqlite:///./bot/src/database/database files/sqlite/
PG_USERNAME=your_pg_username
PG_PASSWORD=your_pg_password
PG_HOST=your_pg_host
PG_PORT=5432
PG_DB_NAME=your_db_name
PG_DB_ROOT_NAME=postgres

# Weather Services
VISUAL_CROSSING_KEY=your_visual_crossing_key
WEATHER_API_KEY=your_weather_api_key
OPEN_WEATHER_MAP_API_KEY=your_openweather_key
```

5. Запустите бота:

```bash
python main.py
```

### Docker установка

1. Убедитесь, что файл `.env` создан

2. Запустите через Docker Compose:

```bash
docker-compose up -d
```

3. Просмотр логов:

```bash
docker-compose logs -f bot
```

## Основные команды бота

-   `/start` - Главное меню
-   `/help` - Список всех команд
-   `/weatherMenu` - Меню погоды
-   `/weatherNow` - Текущая погода
-   `/location` - Управление местоположением
-   `/device` - Выбор устройства для геолокации

## База данных

### Модели

**UserAllInfo**

-   Информация о пользователе (ID, имя, язык)
-   Данные геолокации (город, координаты)
-   Настройки пользователя

**WeatherAllInfo**

-   Кэш погодных данных
-   Сообщения для различных прогнозов

### Репозитории

Все операции с БД инкапсулированы в репозитории:

```python
# Пример использования
user_repo.save_from_telegram_user(user)
user_repo.update_location(user_id, city="Moscow", latitude=55.75, longitude=37.61)
location_exists = user_repo.has_location(user_id)
```

## Сервисы погоды

Бот агрегирует данные из нескольких источников:

1. **YandexParser** - Парсинг Яндекс.Погоды
2. **OpenMeteo** - Бесплатный API погоды
3. **WeatherAPI** - Коммерческий API
4. **VisualCrossing** - Расширенные данные

### Приоритет источников

Система использует приоритетную агрегацию: данные берутся из первого доступного источника в порядке приоритета, с фильтрацией ошибочных значений.

## Кэширование

Redis используется для:

-   Кэширования пользовательских данных
-   Хранения погодных прогнозов (актуальность: 1 час)
-   Оптимизации запросов к БД

## Логирование

Двухуровневая система логирования:

1. **Консоль**: Цветной вывод с детальной информацией
2. **Файлы**: JSON формат для последующего анализа

Логи сохраняются в `bot/logs/` с ротацией по дням.

## Интернационализация

Переводы хранятся в формате Fluent (`.ftl`):

```
bot/src/i18n/
├── ru/
│   ├── text.ftl
│   └── button.ftl
└── en/
    ├── text.ftl
    └── button.ftl
```

Для добавления нового языка создайте соответствующую директорию и файлы переводов.

## Разработка

### Структура middleware

```python
# Инъекция переводов
TranslateMiddleware -> data["locale"]

# Инъекция репозиториев
DataBaseMiddleware -> data["repos"]
```

### Добавление новой команды

1. Создайте обработчик в `src/handlers/user/message.py`
2. Добавьте переводы в `src/i18n/ru/text.ftl`
3. При необходимости создайте клавиатуру в `src/keyboards/`

### Тестирование

Файлы с `if __name__ == "__main__"` можно запускать напрямую для тестирования:

```bash
python bot/src/services/OpenMeteo.py
python bot/src/utils/db_utils.py
```

В возможном будущем напишу тесты для всей программы.

## Производительность

### Оптимизации

-   Пакетные операции с БД
-   Redis кэширование
-   Асинхронные HTTP-запросы
-   Connection pooling для БД

### Мониторинг

Логи содержат:

-   Время выполнения запросов
-   Ошибки и исключения
-   Статистику использования кэша

## Безопасность

-   Переменные окружения для секретов
-   Валидация webhook секретов
-   Санитизация пользовательского ввода
-   Rate limiting для API запросов

## Roadmap

-   [ ] Дополнительные источники погоды
-   [ ] Почасовой прогноз
-   [ ] Утро/Вечер прогноз
-   [ ] 5-дневный прогноз
-   [ ] прогноз Осадков
-   [ ] Ветер/Давление прогноз
-   [ ] Настройки
-   [ ] Подписки на погоду (уведомления)
-   [ ] Добавление английского языка
-   [ ] Графики и визуализации
-   [ ] Админ-панель

Для более подробного описания переходите на доску Trello по ссылке: https://trello.com/b/ZnRVtPRN/my-telegram-bot-all-in-one

## Вклад в проект

Для участия в разработке:

1. Форкните репозиторий
2. Создайте feature-ветку
3. Следуйте PEP8 и основной структуре проекта
4. Добавьте тесты
5. Создайте Pull Request

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## Контакты

Для вопросов и предложений создавайте Issues в репозитории или же пишите в телеграмм который указан в профиле.
