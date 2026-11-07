#!/bin/sh
# Agrosan serverini mustahkamlaydi: xavfsizlik sarlavhalari, nginx versiyasini yashirish,
# www -> agrosan.uz, IP orqali kirishni yopish, 80/443 faqat Cloudflare uchun ochiq.
# server-setup.sh va certbot'dan KEYIN ishga tushiriladi (qayta ishga tushirsa ham bo'ladi):
#   ssh root@IP 'sh -s' < tools/server-xavfsizlik.sh
set -eu

SERT=/etc/letsencrypt/live/agrosan.uz
[ -f "$SERT/fullchain.pem" ] || { echo "Avval certbot bilan sertifikat oling"; exit 1; }

# nginx versiyasi xato sahifalarida ko'rinmasin
rm -f /etc/nginx/conf.d/agrosan-tokens.conf
if grep -qE '^\s*#?\s*server_tokens' /etc/nginx/nginx.conf; then
  sed -i -E 's/^(\s*)#?\s*server_tokens[^;]*;/\1server_tokens off;/' /etc/nginx/nginx.conf
else
  sed -i -E 's/^(\s*http\s*\{)/\1\n\tserver_tokens off;/' /etc/nginx/nginx.conf
fi

# Xavfsizlik sarlavhalari (har bir add_header bor location'ga ham ulanadi)
cat > /etc/nginx/snippets/agrosan-headers.conf <<'EOF'
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://www.googletagmanager.com https://static.cloudflareinsights.com; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com; connect-src 'self' https://cloudflareinsights.com https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests" always;
EOF

cat > /etc/nginx/sites-available/agrosan <<EOF
# IP yoki begona nom bilan kelganlarga hech narsa ko'rsatilmaydi
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    ssl_reject_handshake on;
    return 444;
}

server {
    listen 80;
    listen [::]:80;
    server_name agrosan.uz www.agrosan.uz;
    return 301 https://agrosan.uz\$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name www.agrosan.uz;
    ssl_certificate $SERT/fullchain.pem;
    ssl_certificate_key $SERT/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    return 301 https://agrosan.uz\$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name agrosan.uz;
    root /var/www/agrosan;
    index index.html;
    ssl_certificate $SERT/fullchain.pem;
    ssl_certificate_key $SERT/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    include snippets/agrosan-headers.conf;

    # Sayt uchun kerak bo'lmagan fayllar ochiq ko'rinmasin
    location ~ /\. { deny all; }
    location ^~ /tools/ { deny all; }
    location ^~ /qoralama/ { deny all; }
    location = /CLAUDE.md { deny all; }

    location / { try_files \$uri \$uri/ =404; }

    location ~* \.(jpg|jpeg|png|webp|pdf|css|js)$ {
        expires 7d;
        add_header Cache-Control "public";
        include snippets/agrosan-headers.conf;
    }
    location ~* \.(html|json)$ {
        add_header Cache-Control "no-cache";
        include snippets/agrosan-headers.conf;
    }

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
}
EOF
nginx -t
systemctl reload nginx

# 80/443 faqat Cloudflare'dan: server IP'sini bilgan odam ham Cloudflare'ni aylanib o'ta olmaydi
V4=$(curl -fsS https://www.cloudflare.com/ips-v4)
V6=$(curl -fsS https://www.cloudflare.com/ips-v6)
[ -n "$V4" ] && [ -n "$V6" ] || { echo "Cloudflare IP ro'yxati olinmadi"; exit 1; }
ufw allow OpenSSH >/dev/null
ufw delete allow 'Nginx Full' >/dev/null 2>&1 || true
ufw status numbered | grep -q 'Cloudflare' && \
  ufw status numbered | awk -F'[][]' '/Cloudflare/ {print $2}' | sort -rn | while read -r n; do ufw --force delete "$n" >/dev/null; done
for ip in $V4 $V6; do
  ufw allow proto tcp from "$ip" to any port 80,443 comment Cloudflare >/dev/null
done
ufw --force enable >/dev/null

echo "TAYYOR: sarlavhalar qo'yildi, 80/443 faqat Cloudflare uchun ochiq"
