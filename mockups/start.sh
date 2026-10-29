#!/bin/sh
# Открыть макет: поднять локальный сервер и напечатать ссылки.
cd "$(dirname "$0")" || exit 1
IP=$(ipconfig getifaddr en0 2>/dev/null || echo 127.0.0.1)
echo "Локально:  http://localhost:8080/index.html"
echo "С телефона: http://$IP:8080/index.html"
exec python3 -m http.server 8080 --bind 0.0.0.0
