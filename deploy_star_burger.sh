#!/bin/bash
set -Eeuo pipefail
echo "[!] Загружаю новую версию сайта с GitHub!"
cd /home/star-burger/
git pull > /dev/null
echo "[!] Новые изменения подтянуты из репозитория"
source venv/bin/activate
pip3 install -r requirements.txt > /dev/null
echo "[!] Зависимости установлены!"
npm ci --dev > /dev/null
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./" > /dev/null
rm -r static/
python3 manage.py collectstatic --noinput > /dev/null
echo "[!] Статика для Django собрана!"
python3 manage.py migrate --noinput > /dev/null
echo "[!] База данных отмигрированна!"
systemctl reload nginx.service
systemctl restart star-burger.service
echo "[!] Все зависимые процессы перезагружены!"
echo "$1"
curl -H "X-Rollbar-Access-Token: $2" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "production", "revision": "$(git rev-parse --verify HEAD)", "rollbar_name": "$1", "local_username": "root", "comment": "New deploy", "status": "succeeded"}' > /dev/null
echo "[!] Всё готово"
