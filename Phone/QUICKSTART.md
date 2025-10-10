# 🚀 Быстрый старт - SOS Rescue Mobile App

## 📱 Для пользователей (готовый APK)

### Вариант 1: Скачать и установить (Самый простой)

1. **Скачайте APK** с сервера:
   ```
   https://bashbosh.ru/api/v1/downloads/android
   ```

2. **Включите установку из неизвестных источников:**
   - Настройки → Безопасность → Неизвестные источники ✅

3. **Установите APK:**
   - Откройте скачанный файл
   - Нажмите "Установить"

4. **Войдите в приложение:**
   ```
   Email: citizen@test.ru
   Password: Test1234
   ```

---

## 👨‍💻 Для разработчиков (сборка из исходников)

### Требования:

- ✅ JDK 17 или выше
- ✅ Android Studio Hedgehog (2023.1.1+) или выше
- ✅ Android SDK (API 24-35)
- ✅ ADB (Android Debug Bridge)

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/Yarikttyui/SOS.git
cd SOS/Phone
```

### Шаг 2: Настройте конфигурацию

Файл `gradle.properties` уже настроен для работы с `bashbosh.ru`:

```properties
API_BASE_URL=https://bashbosh.ru
WS_BASE_URL=wss://bashbosh.ru
VERSION_NAME=2.0.0
```

### Шаг 3: Соберите приложение

#### Windows:

```cmd
build-app.bat
```

Или вручную:
```cmd
gradlew clean
gradlew assembleDebug
gradlew assembleRelease
```

#### Linux/Mac:

```bash
./gradlew clean
./gradlew assembleDebug
./gradlew assembleRelease
```

### Шаг 4: Установите на устройство

#### Windows:

```cmd
install-app.bat
```

Или вручную:
```cmd
adb install app/build/outputs/apk/debug/app-debug.apk
```

#### Linux/Mac:

```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## 🔧 Android Studio

### Импорт проекта:

1. Откройте Android Studio
2. File → Open
3. Выберите папку `Phone/`
4. Дождитесь синхронизации Gradle

### Запуск на эмуляторе:

1. Создайте AVD (Android Virtual Device):
   - Tools → Device Manager → Create Device
   - Выберите Pixel 7 Pro
   - Android 13 (API 33) или выше

2. Запустите приложение:
   - Нажмите ▶️ Run
   - Выберите устройство

### Запуск на реальном устройстве:

1. Включите **USB Debugging**:
   - Настройки → О телефоне
   - Нажмите 7 раз на "Номер сборки"
   - Настройки → Для разработчиков → USB-отладка ✅

2. Подключите устройство по USB

3. Разрешите отладку на устройстве

4. Нажмите ▶️ Run в Android Studio

---

## 🧪 Тестирование

### Тестовые аккаунты:

| Роль | Email | Пароль | Описание |
|------|-------|--------|----------|
| Гражданин | `citizen@test.ru` | `Test1234` | Может отправлять SOS |
| Спасатель | `rescuer@test.ru` | `Test1234` | Принимает вызовы |
| Оператор | `operator@test.ru` | `Test1234` | Управляет вызовами |
| Координатор | `coordinator@test.ru` | `Test1234` | Управляет командами |

### Проверка функционала:

#### 1. Вход в систему ✅
```
1. Откройте приложение
2. Введите: citizen@test.ru / Test1234
3. Нажмите "Войти"
```

#### 2. Отправка SOS ✅
```
1. На главном экране нажмите большую красную кнопку "SOS"
2. Выберите тип вызова (медицинский, пожар и т.д.)
3. Введите описание
4. Нажмите "Отправить"
```

#### 3. Просмотр истории ✅
```
1. Прокрутите вниз до "История вызовов"
2. Увидите все ваши прошлые вызовы
```

#### 4. Работа спасателя ✅
```
1. Войдите как rescuer@test.ru
2. Увидите список активных вызовов
3. Нажмите "Принять" на вызове
4. Обновите статус вызова
```

---

## 🐛 Troubleshooting

### Проблема: Приложение не подключается к серверу

**Решение:**
```bash
# Проверьте доступность сервера
curl https://bashbosh.ru/api/v1/

# Должен вернуть: {"message": "SOS Rescue API v1"}
```

### Проблема: Ошибка при сборке "SDK not found"

**Решение:**
```bash
# Создайте local.properties
echo sdk.dir=C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Android\\Sdk > local.properties
```

### Проблема: ADB не находит устройство

**Решение:**
```bash
# Перезапустите ADB
adb kill-server
adb start-server
adb devices
```

### Проблема: "INSTALL_FAILED_UPDATE_INCOMPATIBLE"

**Решение:**
```bash
# Удалите старую версию
adb uninstall com.example.myapplication

# Установите заново
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## 📦 Структура APK

### Debug APK (~15 MB):
- ✅ Логирование включено
- ✅ Отладочные символы
- ✅ Не оптимизирован
- ✅ Для разработки и тестирования

### Release APK (~8 MB):
- ✅ Оптимизирован
- ✅ ProGuard/R8 shrinking
- ✅ Подписан release ключом
- ✅ Для production

---

## 🔐 Безопасность

### HTTPS/WSS соединения:
- ✅ Все запросы через HTTPS
- ✅ WebSocket через WSS
- ✅ SSL/TLS шифрование

### Хранение данных:
- ✅ Токены в SharedPreferences (encrypted)
- ✅ Пароли не сохраняются
- ✅ Биометрия (опционально)

---

## 📊 Мониторинг

### Логи приложения:

```bash
# Все логи
adb logcat | grep "SOS"

# Только ошибки
adb logcat *:E | grep "SOS"

# WebSocket логи
adb logcat | grep "WebSocket"

# API логи
adb logcat | grep "API"
```

### Проверка производительности:

```bash
# CPU usage
adb shell top -n 1 | grep myapplication

# Memory usage  
adb shell dumpsys meminfo com.example.myapplication

# Battery usage
adb shell dumpsys batterystats | grep myapplication
```

---

## 🎯 Дальнейшие шаги

1. ✅ **Установите приложение** на устройство
2. ✅ **Войдите** с тестовым аккаунтом
3. ✅ **Попробуйте отправить SOS** вызов
4. ✅ **Проверьте** историю вызовов
5. ✅ **Войдите как спасатель** и примите вызов
6. ✅ **Проверьте WebSocket** - должны приходить уведомления

---

## 📞 Поддержка

**Возникли проблемы?**

1. Проверьте логи: `adb logcat | grep "SOS"`
2. Проверьте доступность сервера: `curl https://bashbosh.ru/api/v1/`
3. Создайте issue на GitHub с логами

---

## 🎉 Готово!

Приложение настроено и готово к работе с сервером **bashbosh.ru**!

**Основные возможности:**
- ✅ Отправка SOS вызовов
- ✅ Геолокация
- ✅ История вызовов
- ✅ Real-time уведомления
- ✅ Роли: Гражданин, Спасатель, Оператор, Координатор

**Наслаждайтесь использованием! 🚀**
