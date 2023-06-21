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
python3 manage.py collectstatic > /dev/null
echo "[!] Статика для Django собрана!"
python3 manage.py migrate > /dev/null
echo "[!] База данных отмигрированна!"
systemctl reload nginx.service
systemctl restart star-burger.service
echo "[!] Все зависимые процессы перезагружены!"
echo "[!] Всё готово"
