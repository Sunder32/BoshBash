@echo off
echo ========================================
echo  BashBosh Mobile - Quick Rebuild
echo ========================================
echo.

echo [1/3] Cleaning old build...
call gradlew.bat clean

echo.
echo [2/3] Building APK...
call gradlew.bat assembleDebug

echo.
echo [3/3] Done!
echo.
echo APK Location:
echo app\build\outputs\apk\debug\app-debug.apk
echo.
echo To install: adb install -r app\build\outputs\apk\debug\app-debug.apk
echo.
pause
