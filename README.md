# 🚨 BashBosh - Система Экстренного Реагирования

## 📋 О проекте

**BashBosh** — это интеллектуальная система для координации действий спасательных служб с поддержкой веб-интерфейса и мобильного приложения. Платформа обеспечивает мгновенную отправку SOS-сигналов, автоматическое распределение вызовов между спасателями и уведомления в реальном времени через WebSocket.

## ✅ Статус реализации (обновлено 11 октября 2025)

**Backend API**: ✅ FastAPI + SQLAlchemy + WebSocket  
**Frontend UI**: ✅ React + TypeScript + Vite  
**Mobile App**: ✅ Android (Kotlin + Jetpack Compose)  
**База данных**: ✅ SQLite / PostgreSQL / MySQL  
**WebSocket**: ✅ Real-time уведомления и обмен данными  
**Аутентификация**: ✅ JWT токены с защищенными роутами  

---

## � Основные возможности

### 📱 Мобильное приложение (Android)
- **SOS кнопка** — мгновенная отправка сигнала бедствия с геолокацией
- **Громкая сирена** — автоматическое включение при получении вызова (максимальная громкость + вибрация)
- **Push-уведомления** — критические оповещения о новых задачах
- **WebSocket** — связь в реальном времени с сервером
- **Dashboard для спасателей** — просмотр личных задач, командных вызовов и доступных инцидентов
- **Фоновая работа** — Foreground Service для непрерывной работы
- **Автопереподключение** — восстановление WebSocket при разрыве связи

### 💻 Веб-интерфейс
- **Панель оператора** — управление всеми активными вызовами
- **Карта инцидентов** — визуализация SOS-сигналов на карте
- **Управление пользователями** — создание и редактирование учетных записей
- **Система команд** — формирование спасательных групп
- **Статистика** — аналитика по вызовам и производительности
- **Real-time обновления** — автоматическое обновление данных через WebSocket

### 🔐 Роли пользователей
1. **Гражданин** — отправка SOS вызовов через мобильное приложение
2. **Спасатель** — получение и выполнение назначенных задач
3. **Оператор** — управление вызовами и координация команд
4. **Администратор** — полный контроль над системой

### 🌐 Технологии

**Backend:**
- FastAPI 0.104.1 (Python 3.11+)
- SQLAlchemy 2.0 (ORM)
- WebSocket (real-time коммуникация)
- JWT аутентификация (python-jose)
- Поддержка баз данных: SQLite, PostgreSQL, MySQL

**Frontend:**
- React 18 + TypeScript
- Vite (сборщик)
- TailwindCSS (стили)
- Axios (HTTP клиент)
- React Query (управление состоянием)
- Zustand (state management)

**Mobile:**
- Kotlin + Jetpack Compose
- OkHttp (WebSocket клиент)
- Retrofit (HTTP клиент)
- Material 3 Design
- Foreground Service (фоновая работа)

**Инфраструктура:**
- Docker + Docker Compose
- Nginx (reverse proxy + WebSocket)
- Redis (опционально для кеша)
- Celery (опционально для задач)

---

## 🚀 Быстрый старт

### Требования
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
- [app-bubug.apk](./uploads/app-bubug.apk) - продакшн версия
- [app-debug.apk](./uploads/app-debug.apk) - отладочная версия

---

## � Конфигурация

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

---

## 📊 API Endpoints

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

---

## � Структура проекта

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
│   │   │   └── sos_service.py
│   │   └── main.py            # Точка входа
│   ├── alembic/               # Миграции БД
│   ├── uploads/               # Загруженные файлы
│   ├── downloads/             # APK файлы
│   ├── logs/                  # Логи
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/                   # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/        # Переиспользуемые компоненты
│   │   │   ├── BackendStatusPill.tsx
│   │   │   ├── ConfirmDialog.tsx
│   │   │   └── DownloadAppButton.tsx
│   │   ├── features/          # Модули функционала
│   │   │   ├── auth/          # Авторизация
│   │   │   ├── dashboard/     # Дашборды
│   │   │   ├── sos/           # SOS функционал
│   │   │   └── demo/          # Демо
│   │   ├── services/
│   │   │   └── api.ts         # API клиент (Axios)
│   │   ├── store/
│   │   │   └── authStore.ts   # Zustand store
│   │   ├── hooks/             # React hooks
│   │   ├── types/             # TypeScript типы
│   │   ├── utils/             # Утилиты
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env
│
├── Phone/                      # Android приложение
│   ├── app/
│   │   ├── src/main/java/com/example/myapplication/
│   │   │   ├── MainActivity.kt
│   │   │   ├── data/
│   │   │   │   ├── api/
│   │   │   │   │   ├── RescueApiService.kt
│   │   │   │   │   └── RetrofitClient.kt
│   │   │   │   ├── model/
│   │   │   │   │   ├── SOSAlert.kt
│   │   │   │   │   └── User.kt
│   │   │   │   └── preferences/
│   │   │   │       └── PreferencesManager.kt
│   │   │   ├── service/
│   │   │   │   ├── WebSocketManager.kt
│   │   │   │   ├── AlertNotificationService.kt
│   │   │   │   ├── AlertSoundManager.kt
│   │   │   │   └── LocationManager.kt
│   │   │   └── ui/
│   │   │       ├── screen/
│   │   │       │   ├── LoginScreen.kt
│   │   │       │   ├── CitizenDashboard.kt
│   │   │       │   └── RescuerDashboard.kt
│   │   │       └── theme/
│   │   └── build.gradle.kts
│   ├── gradle.properties
│   ├── build-app.bat          # Скрипт сборки
│   └── install-app.bat        # Скрипт установки
│
├── deploy/                     # Деплой конфигурация
│   ├── beget/
│   │   ├── docker-compose.prod.yml
│   │   └── nginx/
│   │       └── frontend.conf  # Nginx с WebSocket
│   └── deploy.sh
│
├── uploads/                    # Папка для APK
│   ├── app-bubug.apk          # Продакшн APK
│   └── app-debug.apk          # Debug APK
│
├── docker-compose.yml          # Docker Compose
├── build-mobile.ps1            # PowerShell скрипт сборки
├── LICENSE
└── README.md                   # Этот файл
```

---

## 🎯 Как это работает

### 1. Отправка SOS (Гражданин через мобильное приложение)

1. Пользователь нажимает кнопку **SOS**
2. Приложение собирает данные:
   - Геолокация (широта, долгота)
   - Тип чрезвычайной ситуации
   - Дополнительная информация
3. Отправка POST запроса на `/api/v1/sos/alerts`
4. Backend создает запись в БД и определяет приоритет

### 2. Распределение задачи

1. Backend анализирует:
   - Геолокацию инцидента
   - Доступных спасателей
   - Загруженность команд
2. Автоматически назначает спасателя или команду
3. Отправляет уведомление через WebSocket

### 3. Получение уведомления (Спасатель)

1. WebSocket соединение получает сообщение
2. Приложение показывает push-уведомление
3. Автоматически включается **громкая сирена**:
   - Максимальная громкость
   - Вибрация по паттерну
   - Зацикленное воспроизведение
4. Спасатель видит детали задачи в dashboard

### 4. Выполнение задачи

1. Спасатель принимает задачу (`POST /alerts/{id}/accept`)
2. Статус меняется на "В процессе"
3. Спасатель выполняет задачу
4. По завершении отмечает как выполненную (`POST /alerts/{id}/complete`)
5. Гражданин получает уведомление о завершении

### 5. WebSocket коммуникация

```
Клиент -> WS Connect: ws://server/api/v1/ws/{user_id}?token={jwt}
Сервер -> Connected: {"type": "connection", "status": "connected"}

[Новый SOS создан оператором]
Сервер -> Спасателю: {
  "type": "new_alert",
  "alert": {
    "id": 123,
    "emergency_type": "fire",
    "location": {...},
    "priority": "high"
  }
}

[Heartbeat каждые 30 секунд]
Клиент -> ping
Сервер -> pong

[Статус изменился]
Сервер -> Всем: {
  "type": "alert_updated",
  "alert_id": 123,
  "status": "in_progress"
}
```

---

## � Безопасность

- ✅ **JWT аутентификация** - токены с истечением срока действия
- ✅ **Bcrypt** - хеширование паролей
- ✅ **HTTPS/WSS** - шифрование трафика (в продакшн)
- ✅ **CORS** - настройка разрешенных источников
- ✅ **SQL Injection защита** - параметризованные запросы (SQLAlchemy)
- ✅ **Rate Limiting** - защита от DDoS (опционально через Nginx)
- ✅ **Валидация данных** - Pydantic схемы
- ✅ **WebSocket аутентификация** - JWT токен в query параметрах

---

## 🚀 Развертывание на production

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

---

## 🧪 Тестирование

### Тестовые аккаунты (после инициализации БД)

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

Используйте инструменты:
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

---

## � Решение проблем

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
4. Проверьте nginx конфигурацию для WebSocket (см. выше)

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

И добавьте heartbeat в коде:
```python
# Backend - уже реализовано
# Клиент отправляет ping каждые 30 секунд
# Сервер отвечает pong
```

---

## 📚 Дополнительные ресурсы

- **FastAPI документация**: https://fastapi.tiangolo.com/
- **React документация**: https://react.dev/
- **Kotlin документация**: https://kotlinlang.org/docs/home.html
- **Jetpack Compose**: https://developer.android.com/jetpack/compose
- **WebSocket RFC**: https://tools.ietf.org/html/rfc6455
- **JWT токены**: https://jwt.io/

---

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Если вы хотите помочь:

1. Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для деталей.

---

## 📞 Контакты и поддержка

- **GitHub**: [Sunder32/BoshBash](https://github.com/Sunder32/BoshBash)
- **Issues**: [Сообщить о проблеме](https://github.com/Sunder32/BoshBash/issues)
- **Website**: https://bashbosh.ru

---

## ⚠️ Важное замечание

**Эта система предназначена для дополнительной поддержки и координации экстренных служб.**  
**В случае реальной чрезвычайной ситуации ВСЕГДА звоните по номеру 112!**

---

## 📸 Скриншоты

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

**Разработано с ❤️ для повышения эффективности работы спасательных служб**

*Версия 1.0.0 | Октябрь 2025*
