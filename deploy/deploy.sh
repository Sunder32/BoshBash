#!/bin/bash

# Скрипт для быстрого деплоя на production

echo "🚀 Начинаем деплой BoshBash..."
echo ""

# Переходим в директорию проекта
cd /opt/sos || exit 1

# Получаем обновления
echo "📥 Получаем обновления из GitHub..."
git pull origin main

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker compose -f deploy/beget/docker-compose.prod.yml down

# Пересобираем контейнеры
echo "🔨 Пересобираем контейнеры..."
docker compose -f deploy/beget/docker-compose.prod.yml build --no-cache

# Запускаем контейнеры
echo "▶️  Запускаем контейнеры..."
docker compose -f deploy/beget/docker-compose.prod.yml up -d

# Ждем 5 секунд
echo "⏳ Ждем запуска сервисов..."
sleep 5

# Проверяем статус
echo ""
echo "📊 Статус контейнеров:"
docker compose -f deploy/beget/docker-compose.prod.yml ps

echo ""
echo "📝 Последние логи:"
docker compose -f deploy/beget/docker-compose.prod.yml logs --tail=20

echo ""
echo "✅ Деплой завершен!"
echo ""
echo "🔍 Проверьте:"
echo "   - https://bash-bosh.ru/login - кнопка входа"
echo "   - https://bash-bosh.ru/register - кнопка регистрации"
echo ""
echo "💡 Не забудьте сделать жесткую перезагрузку (Ctrl+Shift+R) в браузере!"
