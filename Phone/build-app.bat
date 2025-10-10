@echo off
REM ========================================
REM SOS Rescue App - Build Script
REM ========================================

echo.
echo ============================================
echo   SOS Rescue App - Mobile Build Script
echo ============================================
echo.

REM Проверка Java
echo [1/5] Checking Java...
java -version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Java not found! Please install JDK 17+
    pause
    exit /b 1
)
echo [OK] Java detected

REM Очистка предыдущих сборок
echo.
echo [2/5] Cleaning previous builds...
call gradlew clean
if errorlevel 1 (
    echo [ERROR] Clean failed!
    pause
    exit /b 1
)
echo [OK] Clean completed

REM Сборка Debug APK
echo.
echo [3/5] Building Debug APK...
call gradlew assembleDebug
if errorlevel 1 (
    echo [ERROR] Debug build failed!
    pause
    exit /b 1
)
echo [OK] Debug APK built successfully

REM Сборка Release APK
echo.
echo [4/5] Building Release APK...
call gradlew assembleRelease
if errorlevel 1 (
    echo [ERROR] Release build failed!
    pause
    exit /b 1
)
echo [OK] Release APK built successfully

REM Показать результаты
echo.
echo [5/5] Build Summary:
echo ============================================
echo.
echo Debug APK:
dir /B app\build\outputs\apk\debug\*.apk 2>nul
if errorlevel 1 (
    echo   Not found
) else (
    for %%F in (app\build\outputs\apk\debug\*.apk) do echo   %%~nxF (%%~zF bytes)
)

echo.
echo Release APK:
dir /B app\build\outputs\apk\release\*.apk 2>nul
if errorlevel 1 (
    echo   Not found
) else (
    for %%F in (app\build\outputs\apk\release\*.apk) do echo   %%~nxF (%%~zF bytes)
)

echo.
echo ============================================
echo   Build completed successfully!
echo ============================================
echo.
echo Next steps:
echo   1. Install Debug: adb install app\build\outputs\apk\debug\app-debug.apk
echo   2. Or install Release: adb install app\build\outputs\apk\release\app-release.apk
echo.

pause
