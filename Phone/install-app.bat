@echo off
REM ========================================
REM SOS Rescue App - Install Script
REM ========================================

echo.
echo ============================================
echo   SOS Rescue App - Installation Script
echo ============================================
echo.

REM Проверка ADB
echo [*] Checking ADB...
adb version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ADB not found!
    echo Please install Android SDK Platform-Tools
    echo Download: https://developer.android.com/studio/releases/platform-tools
    pause
    exit /b 1
)
echo [OK] ADB detected

REM Проверка подключенных устройств
echo.
echo [*] Checking connected devices...
adb devices | findstr "device" | findstr /v "List" >nul
if errorlevel 1 (
    echo [ERROR] No devices connected!
    echo.
    echo Please:
    echo   1. Connect your Android device via USB
    echo   2. Enable USB Debugging in Developer Options
    echo   3. Allow USB debugging on device popup
    pause
    exit /b 1
)

echo [OK] Device connected:
adb devices
echo.

REM Выбор версии
echo Choose version to install:
echo   1. Debug (for testing)
echo   2. Release (for production)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    set APK_PATH=app\build\outputs\apk\debug\app-debug.apk
    set VERSION=Debug
) else if "%choice%"=="2" (
    set APK_PATH=app\build\outputs\apk\release\app-release.apk
    set VERSION=Release
) else (
    echo [ERROR] Invalid choice!
    pause
    exit /b 1
)

REM Проверка наличия APK
if not exist "%APK_PATH%" (
    echo [ERROR] APK not found: %APK_PATH%
    echo.
    echo Please build the app first:
    echo   Run: build-app.bat
    pause
    exit /b 1
)

REM Удаление старой версии (опционально)
echo.
echo [*] Checking for existing installation...
adb shell pm list packages | findstr "com.example.myapplication" >nul
if not errorlevel 1 (
    echo [*] Uninstalling old version...
    adb uninstall com.example.myapplication
)

REM Установка APK
echo.
echo [*] Installing %VERSION% APK...
adb install "%APK_PATH%"
if errorlevel 1 (
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Installation completed successfully!
echo ============================================
echo.
echo App installed: SOS Rescue v2.0
echo Package: com.example.myapplication
echo Server: https://bashbosh.ru
echo.
echo The app should now appear on your device
echo.

pause
