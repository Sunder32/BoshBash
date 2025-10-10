# Инструкция по пересборке мобильного приложения

## Проблема
После изменения URL сервера в gradle.properties нужно пересобрать APK.

## Решение

### 1. Очистка и пересборка (Windows PowerShell)

```powershell
cd Phone
.\gradlew clean assembleDebug
```

### 2. После успешной сборки APK будет находиться в:
```
Phone\app\build\outputs\apk\debug\app-debug.apk
```

### 3. Установка на устройство

#### Через USB:
```powershell
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

#### Или скопируйте app-debug.apk на телефон и установите вручную

## Что было исправлено

### В gradle.properties изменены URL:
- ✅ `API_BASE_URL=http://bashbosh.ru:8000` (было https)
- ✅ `WS_BASE_URL=ws://bashbosh.ru:8000` (было wss)
- ✅ `API_FALLBACK_URL=http://bashbosh.ru:8000` (было http://10.0.2.2:8000)
- ✅ `WS_FALLBACK_URL=ws://bashbosh.ru:8000` (было ws://10.0.2.2:8000)

## Функции приложения

### Кнопка выхода
✅ Есть в обоих дашбордах (Citizen и Rescuer)
- Находится в правом верхнем углу карточки профиля
- Иконка ExitToApp (стрелка выхода)

### Отправка SOS
✅ Функция работает правильно:
1. Нажмите на красную кнопку SOS или выберите тип происшествия
2. Заполните описание (минимум 10 символов)
3. Нажмите "Отправить SOS"
4. Алерт будет отправлен на сервер с вашими координатами

## API Endpoints
Приложение использует правильные endpoints:
- Login: `POST /api/v1/auth/login`
- Get User: `GET /api/v1/auth/me`
- Create Alert: `POST /api/v1/sos`
- Get Alerts: `GET /api/v1/sos`
- Update Alert: `PATCH /api/v1/sos/{id}`

## Тестовые аккаунты

### Гражданин (отправка SOS):
- Email: `citizen@test.ru`
- Password: `Test1234`

### Спасатель (получение и обработка алертов):
- Email: `rescuer1@test.ru`
- Password: `Test1234`

### Администратор:
- Email: `admin@test.ru`
- Password: `Test1234`

## Разрешения
Приложению нужны разрешения на:
- 📍 Геолокацию (для отправки координат в SOS)
- 🔔 Уведомления (для получения алертов)
- 📷 Камеру (опционально, для фото с места происшествия)

При первом запуске разрешите все запрошенные разрешения.
