# BashBosh - Система Экстренного Реагирования

<div align="center">
  <h3 style="color: #9ca3af;">В РАЗРАБОТКЕ ПРОЕКТА УЧАСТВОВАЛИ: Заволокин Михаил, Гаран Ярослав, Дедюхин Денис.</h3>
</div>

## Описание

**BashBosh** — это интеллектуальная система для координации действий спасательных служб с поддержкой веб-интерфейса и мобильного приложения. Платформа обеспечивает мгновенную отправку SOS-сигналов, автоматическое распределение вызовов между спасателями и уведомления в реальном времени через WebSocket.

## Статус реализации

По состоянию на 11 октября 2025 года все основные компоненты системы полностью реализованы:

- **Backend API** — FastAPI + SQLAlchemy + WebSocket
- **Frontend UI** — React + TypeScript + Vite
- **Mobile App** — Android (Kotlin + Jetpack Compose)
- **База данных** — SQLite / PostgreSQL / MySQL
- **WebSocket** — Real-time уведомления и обмен данными
- **Аутентификация** — JWT токены с защищенными роутами

## Основные возможности

### Мобильное приложение (Android)
- **SOS кнопка** — мгновенная отправка сигнала бедствия с геолокацией
- **Громкая сирена** — автоматическое включение при получении вызова (максимальная громкость + вибрация)
- **Push-уведомления** — критические оповещения о новых задачах
- **WebSocket соединение** — связь в реальном времени с сервером
- **Dashboard для спасателей** — просмотр личных задач, командных вызовов и доступных инцидентов
- **Фоновая работа** — Foreground Service для непрерывной работы
- **Автопереподключение** — восстановление WebSocket при разрыве связи

### Веб-интерфейс
- **Панель оператора** — управление всеми активными вызовами
- **Карта инцидентов** — визуализация SOS-сигналов на карте
- **Управление пользователями** — создание и редактирование учетных записей
- **Система команд** — формирование спасательных групп
- **Статистика** — аналитика по вызовам и производительности
- **Real-time обновления** — автоматическое обновление данных через WebSocket

### Роли пользователей
1. **Гражданин** — отправка SOS вызовов через мобильное приложение
2. **Спасатель** — получение и выполнение назначенных задач
3. **Оператор** — управление вызовами и координация команд
4. **Администратор** — полный контроль над системой

## Технологический стек

### Backend
- **FastAPI 0.104.1** — современный Python веб-фреймворк (Python 3.11+)
- **SQLAlchemy 2.0** — ORM для работы с базами данных
- **WebSocket** — real-time коммуникация
- **JWT аутентификация** — python-jose для безопасной аутентификации
- **Поддержка баз данных** — SQLite, PostgreSQL, MySQL

### Frontend
- **React 18** — библиотека для создания пользовательских интерфейсов
- **TypeScript** — типизированный JavaScript
- **Vite** — быстрый сборщик проектов
- **TailwindCSS** — utility-first CSS фреймворк
- **Axios** — HTTP клиент
- **React Query** — управление серверным состоянием
- **Zustand** — легковесный state management

### Mobile
- **Kotlin** — современный язык для Android разработки
- **Jetpack Compose** — декларативный UI toolkit
- **OkHttp** — WebSocket клиент
- **Retrofit** — HTTP клиент
- **Material 3 Design** — система дизайна Google
- **Foreground Service** — фоновая работа приложения

### Инфраструктура
- **Docker + Docker Compose** — контейнеризация приложений
- **Nginx** — reverse proxy + поддержка WebSocket
- **Redis** — кеширование (опционально)
- **Celery** — асинхронные задачи (опционально)

## Быстрый старт

### Системные требования
- Python 3.11+
- Node.js 18+
- Docker и Docker Compose (для контейнеризации)
- Android Studio (для сборки мобильного приложения)

### Вариант 1: Запуск через Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com/Sunder32/BoshBash.git
cd BoshBash

# Настроить переменные окружения
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Запустить все сервисы
docker-compose up -d

# Применить миграции базы данных
docker-compose exec backend alembic upgrade head

# Открыть в браузере
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Вариант 2: Ручной запуск

#### Backend

```powershell
cd backend

# Создать виртуальное окружение
python -m venv venv
.\venv\Scripts\Activate.ps1

# Установить зависимости
pip install -r requirements.txt

# Настроить .env файл
cp .env.example .env
# Отредактировать .env (DATABASE_URL, SECRET_KEY и т.д.)

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend будет доступен:**
- API: http://localhost:8000
- WebSocket: ws://localhost:8000/api/v1/ws/{user_id}?token={jwt_token}
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Frontend

```powershell
cd frontend

# Установить зависимости
npm install

# Настроить .env файл
cp .env.example .env
# Отредактировать VITE_API_URL и другие переменные

# Запустить dev сервер
npm run dev
```

**Frontend будет доступен:** http://localhost:3000 (или порт из Vite)

#### Mobile App (Android)

```powershell
cd Phone

# Настроить gradle.properties
cp gradle.properties.example gradle.properties
# Отредактировать API_BASE_URL и WS_BASE_URL

# Собрать APK
.\gradlew assembleDebug

# APK будет в:
# Phone\app\build\outputs\apk\debug\app-debug.apk

# Установить на устройство через USB
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

**Или скачать готовый APK:**
- app-bubug.apk - продакшн версия
- app-debug.apk - отладочная версия

## Конфигурация

### Backend (.env)

```env
# Приложение
APP_NAME="BashBosh Rescue System"
APP_VERSION="1.0.0"

# База данных (выбрать один вариант)
DATABASE_URL=sqlite:///./rescue.db
# DATABASE_URL=postgresql://user:pass@localhost:5432/rescue_db
# DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/rescue_db

# Безопасность
SECRET_KEY=your-super-secret-key-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Геолокация (по умолчанию)
DEFAULT_LOCATION_LAT=55.7558
DEFAULT_LOCATION_LON=37.6173

# Redis (опционально)
REDIS_URL=redis://localhost:6379/0

# Email (опционально)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend (.env)

```env
# API URL
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Mapbox (опционально)
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

### Mobile (gradle.properties)

```properties
# Production
API_BASE_URL=https://bashbosh.ru
WS_BASE_URL=wss://bashbosh.ru

# Fallback (для эмулятора)
API_FALLBACK_URL=http://10.0.2.2:8000
WS_FALLBACK_URL=ws://10.0.2.2:8000

# Version
VERSION_NAME=1.0.0
VERSION_CODE=1
```

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Регистрация нового пользователя
- `POST /login` - Вход и получение JWT токена
- `POST /refresh` - Обновление токена
- `GET /me` - Информация о текущем пользователе
- `POST /logout` - Выход из системы

### SOS Alerts (`/api/v1/sos`)
- `POST /alerts` - Создать SOS тревогу
- `GET /alerts` - Список всех тревог (с фильтрацией по ролям)
- `GET /alerts/{id}` - Детали конкретной тревоги
- `PATCH /alerts/{id}` - Обновить статус тревоги
- `DELETE /alerts/{id}` - Удалить тревогу (только админ)
- `POST /alerts/{id}/assign` - Назначить спасателя на задачу
- `POST /alerts/{id}/accept` - Принять задачу (спасатель)
- `POST /alerts/{id}/complete` - Завершить задачу

### Users (`/api/v1/users`)
- `GET /` - Список всех пользователей
- `GET /{id}` - Профиль пользователя
- `PATCH /{id}` - Обновить профиль
- `DELETE /{id}` - Удалить пользователя
- `GET /rescuers` - Список всех спасателей

### Teams (`/api/v1/teams`)
- `POST /` - Создать команду
- `GET /` - Список команд
- `GET /{id}` - Детали команды
- `PATCH /{id}` - Обновить команду
- `DELETE /{id}` - Удалить команду
- `POST /{id}/members` - Добавить участника
- `DELETE /{id}/members/{user_id}` - Удалить участника

### Notifications (`/api/v1/notifications`)
- `GET /` - Список уведомлений текущего пользователя
- `GET /{id}` - Детали уведомления
- `POST /{id}/read` - Отметить как прочитанное
- `POST /read-all` - Отметить все как прочитанные

### WebSocket (`/api/v1/ws`)
- `WS /{user_id}?token={jwt}` - Подключение к WebSocket каналу
  - Получение real-time уведомлений
  - Обновления статусов тревог
  - Heartbeat (ping/pong)

### Downloads (`/api/v1/downloads`)
- `GET /android` - Скачать Android APK
- `GET /android/metadata` - Метаданные APK (версия, размер, hash)

## Структура проекта

```
BoshBash/
├── backend/                    # Backend API (FastAPI)
│   ├── app/
│   │   ├── api/v1/            # API роуты
│   │   │   ├── auth.py        # Аутентификация
│   │   │   ├── sos.py         # SOS вызовы
│   │   │   ├── users.py       # Пользователи
│   │   │   ├── teams.py       # Команды
│   │   │   ├── notifications.py
│   │   │   ├── websocket.py   # WebSocket
│   │   │   └── downloads.py   # Скачивание APK
│   │   ├── core/
│   │   │   ├── config.py      # Конфигурация
│   │   │   ├── database.py    # База данных
│   │   │   └── security.py    # Безопасность и JWT
│   │   ├── models/            # SQLAlchemy модели
│   │   ├── schemas/           # Pydantic схемы
│   │   ├── services/          # Бизнес-логика
│   │   │   ├── websocket_service.py
│   │   │   ├── notification_service.py
│   │   │   └── alert_service.py
│   │   └── main.py            # Точка входа
│   ├── alembic/               # Миграции БД
│   ├── tests/                 # Тесты
│   ├── requirements.txt       # Python зависимости
│   └── .env.example           # Пример конфигурации
│
├── frontend/                  # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/        # React компоненты
│   │   ├── pages/             # Страницы
│   │   ├── services/          # API клиенты
│   │   ├── hooks/             # React hooks
│   │   ├── store/             # Zustand store
│   │   ├── types/             # TypeScript типы
│   │   └── App.tsx            # Главный компонент
│   ├── public/                # Статические файлы
│   ├── package.json           # Node.js зависимости
│   └── .env.example           # Пример конфигурации
│
├── Phone/                     # Mobile App (Android)
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/bashbosh/
│   │   │   │   ├── ui/        # Compose UI
│   │   │   │   ├── data/      # Repositories
│   │   │   │   ├── domain/    # Use cases
│   │   │   │   ├── network/   # API & WebSocket
│   │   │   │   └── service/   # Foreground Service
│   │   │   ├── res/           # Ресурсы
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle       # Gradle конфигурация
│   ├── gradle.properties      # Gradle properties
│   └── gradle.properties.example
│
├── deploy/                    # Deployment конфигурации
│   ├── beget/
│   │   ├── docker-compose.prod.yml
│   │   └── nginx.conf
│   └── scripts/               # Деплой скрипты
│
├── uploads/                   # APK файлы для скачивания
│   ├── app-bubug.apk
│   └── app-debug.apk
│
├── docker-compose.yml         # Docker Compose для разработки
└── README.md                  # Документация
```

## WebSocket протокол

### Подключение клиента

```javascript
// Пример подключения через JavaScript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/1?token=YOUR_JWT_TOKEN');

ws.onopen = () => {
  console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket connection closed');
};
```

### Типы сообщений

**Heartbeat (ping/pong):**
```
Клиент -> ping
Сервер -> pong
```

**Уведомление о новой тревоге:**
```json
{
  "type": "new_alert",
  "alert_id": 123,
  "emergency_type": "fire",
  "location": {
    "latitude": 55.7558,
    "longitude": 37.6173
  },
  "description": "Пожар в квартире"
}
```

**Обновление статуса:**
```json
{
  "type": "alert_updated",
  "alert_id": 123,
  "status": "in_progress",
  "assigned_to": {
    "id": 456,
    "full_name": "Иван Иванов"
  }
}
```

**Назначение задачи:**
```json
{
  "type": "task_assigned",
  "alert_id": 123,
  "message": "Вам назначена новая задача"
}
```

## Безопасность

Система реализует многоуровневую защиту:

- **JWT аутентификация** — токены с истечением срока действия
- **Bcrypt** — хеширование паролей с использованием соли
- **HTTPS/WSS** — шифрование трафика в продакшн окружении
- **CORS** — настройка разрешенных источников
- **SQL Injection защита** — параметризованные запросы через SQLAlchemy
- **Rate Limiting** — защита от DDoS атак (через Nginx)
- **Валидация данных** — строгая проверка входных данных через Pydantic
- **WebSocket аутентификация** — JWT токен в query параметрах

## Развертывание на production

### Настройка nginx для WebSocket

```nginx
# /etc/nginx/sites-available/bashbosh

upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name bashbosh.ru www.bashbosh.ru;

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /api/v1/ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
```

### Docker Production

```bash
# Собрать и запустить
docker-compose -f deploy/beget/docker-compose.prod.yml up -d

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f frontend

# Применить миграции
docker-compose exec backend alembic upgrade head

# Остановить
docker-compose down
```

### Переменные окружения для production

**backend/.env.production:**
```env
APP_NAME="BashBosh Rescue System"
DATABASE_URL=postgresql://user:password@postgres:5432/rescue_db
SECRET_KEY=very-long-random-secret-key-min-32-chars
CORS_ORIGINS=["https://bashbosh.ru"]
REDIS_URL=redis://:password@redis:6379/0
```

**frontend/.env.production:**
```env
VITE_API_URL=https://bashbosh.ru
VITE_WS_URL=wss://bashbosh.ru
```

## Тестирование

### Тестовые аккаунты

После инициализации базы данных доступны следующие тестовые учетные записи:

```
Гражданин:     citizen@test.ru   / Test1234
Спасатель:     rescuer@test.ru   / Test1234
Оператор:      operator@test.ru  / Test1234
Администратор: admin@test.ru     / Test1234
```

### Проверка API через curl

```bash
# Регистрация
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234",
    "full_name": "Test User",
    "role": "citizen"
  }'

# Вход
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234"
  }'

# Получить текущего пользователя
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Создать SOS
curl -X POST http://localhost:8000/api/v1/sos/alerts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_type": "fire",
    "description": "Пожар в квартире",
    "latitude": 55.7558,
    "longitude": 37.6173
  }'
```

### WebSocket тестирование

Используйте следующие инструменты для тестирования WebSocket соединений:

- **websocat**: `websocat ws://localhost:8000/api/v1/ws/1?token=YOUR_JWT`
- **Postman**: WebSocket request
- Браузерная консоль:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/1?token=YOUR_JWT');

ws.onopen = () => console.log('Connected');
ws.onmessage = (event) => console.log('Message:', JSON.parse(event.data));
ws.onclose = () => console.log('Disconnected');
ws.onerror = (error) => console.error('Error:', error);

// Отправить ping
ws.send('ping');
```

## Решение проблем

### Backend не запускается

**Проблема:** `ModuleNotFoundError: No module named 'XXX'`

**Решение:**
```bash
cd backend
pip install -r requirements.txt
```

**Проблема:** `sqlalchemy.exc.OperationalError: unable to open database file`

**Решение:**
```bash
# Создать директорию для БД
mkdir -p backend
cd backend
alembic upgrade head
```

### Frontend не собирается

**Проблема:** `Error: Cannot find module 'XXX'`

**Решение:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Проблема:** PostCSS ошибки

**Решение:** Убедитесь что `postcss.config.js` использует `export default`:
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Mobile App не подключается к серверу

**Проблема:** WebSocket 404 или Connection refused

**Решение:**
1. Проверьте `gradle.properties` - правильные URL
2. Если используете эмулятор: `http://10.0.2.2:8000` вместо `localhost`
3. Если реальное устройство: используйте IP компьютера в локальной сети
4. Проверьте nginx конфигурацию для WebSocket

**Проблема:** Сирена не играет

**Решение:**
1. Проверьте разрешения в AndroidManifest.xml
2. Убедитесь что Foreground Service запущен
3. Проверьте настройки "Не беспокоить" на устройстве

### WebSocket отключается

**Проблема:** Connection closes after 60 seconds

**Решение:** Настройте timeout в nginx:
```nginx
proxy_read_timeout 3600s;
proxy_send_timeout 3600s;
```

И добавьте heartbeat в коде (уже реализовано - клиент отправляет ping каждые 30 секунд, сервер отвечает pong)

## Дополнительные ресурсы

- **FastAPI документация** - https://fastapi.tiangolo.com/
- **React документация** - https://react.dev/
- **Kotlin документация** - https://kotlinlang.org/docs/home.html
- **Jetpack Compose** - https://developer.android.com/jetpack/compose
- **WebSocket RFC** - https://tools.ietf.org/html/rfc6455
- **JWT токены** - https://jwt.io/

## Вклад в проект

Мы приветствуем вклад в развитие проекта! Если вы хотите помочь:

1. Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для деталей.

## Контакты и поддержка

- **GitHub** - Sunder32/BoshBash
- **Issues** - Сообщить о проблеме через GitHub Issues
- **Website** - https://bashbosh.ru

## Важное замечание

**Эта система предназначена для дополнительной поддержки и координации экстренных служб.**

**В случае реальной чрезвычайной ситуации ВСЕГДА звоните по номеру 112!**

## Функциональность приложения

### Мобильное приложение
- Dashboard спасателя с активными задачами
- Кнопка SOS для граждан
- Push-уведомления о новых вызовах
- История выполненных задач

### Веб-интерфейс
- Панель оператора с картой инцидентов
- Управление пользователями и командами
- Статистика и аналитика
- Real-time обновления через WebSocket

---

**Разработано для повышения эффективности работы спасательных служб**

*Версия 1.0.0 | Октябрь 2025*
