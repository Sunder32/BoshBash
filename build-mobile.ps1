# Скрипт для пересборки мобильного приложения

Write-Host "🔨 Начинаем пересборку мобильного приложения..." -ForegroundColor Cyan
Write-Host ""

# Переходим в директорию Phone
Set-Location -Path "Phone"

Write-Host "🧹 Очистка предыдущей сборки..." -ForegroundColor Yellow
.\gradlew clean

Write-Host ""
Write-Host "🔧 Сборка APK (debug)..." -ForegroundColor Yellow
.\gradlew assembleDebug

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Сборка успешно завершена!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 APK находится в:" -ForegroundColor Cyan
    Write-Host "   Phone\app\build\outputs\apk\debug\app-debug.apk" -ForegroundColor White
    Write-Host ""
    Write-Host "📲 Установка на устройство:" -ForegroundColor Cyan
    Write-Host "   adb install -r app\build\outputs\apk\debug\app-debug.apk" -ForegroundColor White
    Write-Host ""
    
    # Проверяем подключенные устройства
    $devices = adb devices
    if ($devices -match "device$") {
        Write-Host "📱 Обнаружены подключенные устройства" -ForegroundColor Green
        Write-Host "Хотите установить APK сейчас? (Y/N)" -ForegroundColor Yellow
        $response = Read-Host
        
        if ($response -eq "Y" -or $response -eq "y") {
            Write-Host "📲 Установка APK..." -ForegroundColor Cyan
            adb install -r app\build\outputs\apk\debug\app-debug.apk
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "✅ Приложение успешно установлено!" -ForegroundColor Green
            } else {
                Write-Host ""
                Write-Host "❌ Ошибка установки" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "📱 Устройства не подключены. Скопируйте APK на телефон вручную." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "❌ Ошибка сборки!" -ForegroundColor Red
    Write-Host "Проверьте логи выше для деталей" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔙 Возврат в корневую директорию..." -ForegroundColor Cyan
Set-Location -Path ".."

Write-Host ""
Write-Host "✨ Готово!" -ForegroundColor Green
