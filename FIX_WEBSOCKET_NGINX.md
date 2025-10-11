# 🔧 Исправление WebSocket - Инструкция

## ❌ Проблема
Мобильное приложение НЕ получает уведомления через WebSocket, потому что nginx не проксирует запросы к `/api/v1/ws/`!

**Логи показывают:**
```
WebSocketManager: ❌ WebSocket connection failed: Expected HTTP 101 response but was '404 Not Found'
Connecting to: ws://84.54.30.211/api/v1/ws/a5723fbe-36ad-403b-9b05-aa3b1d6aa92f
```

## ✅ Решение
Добавлена конфигурация nginx для проксирования WebSocket на `/api/v1/ws/`.

## 📝 Что нужно сделать

### 1. Подключиться к серверу
```bash
ssh your-user@84.54.30.211
```

### 2. Перейти в директорию проекта
```bash
cd /path/to/your/project/deploy/beget
```

### 3. Перезапустить контейнеры с nginx
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Проверить логи nginx
```bash
docker-compose -f docker-compose.prod.yml logs -f web
```

Должно быть видно, что nginx загрузил новую конфигурацию.

### 5. Проверить WebSocket подключение

Попробуйте подключиться с помощью curl:
```bash
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  "http://84.54.30.211/api/v1/ws/a5723fbe-36ad-403b-9b05-aa3b1d6aa92f?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhNTcyM2ZiZS0zNmFkLTQwM2ItOWIwNS1hYTNiMWQ2YWE5MmYiLCJyb2xlIjoicmVzY3VlciIsImV4cCI6MTc2MDE1OTM3NCwidHlwZSI6ImFjY2VzcyJ9.9_y_lWHQ8QEoV4WDns-rfidQ-ektYoWOC812UEKWFBo"
```

**Ожидаемый результат:** HTTP 101 Switching Protocols (вместо 404)

## 🔍 Что изменилось в nginx конфигурации

**Было:**
```nginx
location /api/ {
    proxy_pass http://backend:8000;
    ...
}

location /ws/ {
    proxy_pass http://backend:8000/ws/;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
}
```

**Стало:**
```nginx
# NEW! WebSocket для мобильного приложения (ДОЛЖЕН БЫТЬ ПЕРЕД /api/)
location /api/v1/ws/ {
    proxy_pass http://backend:8000/api/v1/ws/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
    proxy_read_timeout 86400;
    proxy_send_timeout 86400;
}

location /api/ {
    proxy_pass http://backend:8000;
    ...
}

location /ws/ {
    proxy_pass http://backend:8000/ws/;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
}
```

## 📱 После перезапуска nginx

### Переустановите приложение на телефоне
```powershell
cd Phone
.\gradlew assembleDebug
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

### Проверьте логи приложения
```powershell
adb logcat | Select-String "WebSocket"
```

**Ожидаемый результат:**
```
WebSocketManager: ✅ WebSocket connected successfully!
```

## 🎉 Проверка работы

1. **Запустите приложение** на телефоне как спасатель
2. **На операторе** назначьте новый вызов на эту команду
3. **На телефоне** должна:
   - Появиться **notification** с новым вызовом
   - **Заиграть сирена** 🚨
   - Обновиться список вызовов

## 🐛 Если все равно не работает

Проверьте логи бэкенда:
```bash
docker-compose -f docker-compose.prod.yml logs -f backend
```

Должны быть сообщения:
```
INFO: WebSocket connection attempt for user a5723fbe-36ad-403b-9b05-aa3b1d6aa92f
INFO: WebSocket connected for user a5723fbe-36ad-403b-9b05-aa3b1d6aa92f
```

Если видите ошибки аутентификации, проверьте, что токен валидный.
