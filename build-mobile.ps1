# Скрипт для пересборки мобильного приложения

Write-Host "🔨 Начинаем пересборку мобильного приложения..." -ForegroundColor Cyan
Write-Host ""

# Переходим в директорию Phone
Set-Location -Path "Phone"

Write-Host "🧹 Очистка предыдущей сборки..." -ForegroundColor Yellow
.\gradlew clean

Write-Host ""
Write-Host "🔧 Сборка APK (release)..." -ForegroundColor Yellow
.\gradlew assembleRelease

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Сборка успешно завершена!" -ForegroundColor Green
    
    # Копируем APK в папку downloads
    $apkSource = "app\build\outputs\apk\release\app-release.apk"
    $apkDest = "..\downloads\sos-mobile-latest.apk"
    $metadataDest = "..\downloads\android-metadata.json"
    
    if (Test-Path $apkSource) {
        Write-Host ""
        Write-Host "📦 Копирование APK в папку downloads..." -ForegroundColor Cyan
        
        # Создаем папку downloads если её нет
        if (-not (Test-Path "..\downloads")) {
            New-Item -Path "..\downloads" -ItemType Directory | Out-Null
        }
        
        Copy-Item -Path $apkSource -Destination $apkDest -Force
        
        # Получаем информацию о файле
        $apkFile = Get-Item $apkSource
        $fileSize = $apkFile.Length
        $fileHash = (Get-FileHash -Path $apkSource -Algorithm SHA256).Hash.ToLower()
        $timestamp = (Get-Date).ToUniversalTime().ToString("o")
        
        # Создаем файл метаданных
        $metadata = @{
            filename = "sos-mobile-latest.apk"
            version_name = "1.0.0"
            version_code = 1
            size_bytes = $fileSize
            updated_at = $timestamp
            sha256 = $fileHash
        }
        
        $metadata | ConvertTo-Json | Set-Content -Path $metadataDest -Encoding UTF8
        
        Write-Host "✅ APK скопирован: downloads\sos-mobile-latest.apk" -ForegroundColor Green
        Write-Host "✅ Метаданные созданы: downloads\android-metadata.json" -ForegroundColor Green
        Write-Host "   Размер: $([math]::Round($fileSize / 1MB, 2)) МБ" -ForegroundColor White
        Write-Host "   SHA256: $fileHash" -ForegroundColor White
    } else {
        Write-Host "❌ APK файл не найден в $apkSource" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "📦 APK находится в:" -ForegroundColor Cyan
    Write-Host "   Phone\app\build\outputs\apk\release\app-release.apk" -ForegroundColor White
    Write-Host "   downloads\sos-mobile-latest.apk" -ForegroundColor White
    Write-Host ""
    Write-Host "📲 Установка на устройство:" -ForegroundColor Cyan
    Write-Host "   adb install -r app\build\outputs\apk\release\app-release.apk" -ForegroundColor White
    Write-Host ""
    
    # Проверяем подключенные устройства
    $devices = adb devices
    if ($devices -match "device$") {
        Write-Host "📱 Обнаружены подключенные устройства" -ForegroundColor Green
        Write-Host "Хотите установить APK сейчас? (Y/N)" -ForegroundColor Yellow
        $response = Read-Host
        
        if ($response -eq "Y" -or $response -eq "y") {
            Write-Host "📲 Установка APK..." -ForegroundColor Cyan
            adb install -r app\build\outputs\apk\release\app-release.apk
            
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
