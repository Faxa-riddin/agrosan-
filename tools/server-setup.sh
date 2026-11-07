#!/bin/sh
# Agrosan saytini yangi Ubuntu VPS'ga o'rnatadi: nginx, xavfsizlik devori, avtomatik yangilanish
# Ishga tushirish: ssh root@IP 'sh -s' < tools/server-setup.sh
set -eu

export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq nginx git ufw certbot python3-certbot-nginx unattended-upgrades

# Sayt GitHub'dagi repodan olinadi
if [ -d /var/www/agrosan/.git ]; then
  git -C /var/www/agrosan pull -q --ff-only
else
  git clone -q https://github.com/Faxa-riddin/agrosan-.git /var/www/agrosan
fi

cat > /etc/nginx/sites-available/agrosan <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name agrosan.uz www.agrosan.uz;
    root /var/www/agrosan;
    index index.html;

    # Sayt uchun kerak bo'lmagan fayllar ochiq ko'rinmasin
    location ~ /\. { deny all; }
    location ^~ /tools/ { deny all; }
    location ^~ /qoralama/ { deny all; }
    location = /CLAUDE.md { deny all; }

    location / { try_files $uri $uri/ =404; }

    location ~* \.(jpg|jpeg|png|webp|pdf|css|js)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
    location ~* \.(html|json)$ { add_header Cache-Control "no-cache"; }

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
}
EOF
ln -sf /etc/nginx/sites-available/agrosan /etc/nginx/sites-enabled/agrosan
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl enable --now nginx
systemctl reload nginx

# Faqat SSH kalit bilan kirish
printf 'PasswordAuthentication no
' > /etc/ssh/sshd_config.d/00-agrosan.conf
sshd -t && systemctl reload ssh

ufw allow OpenSSH >/dev/null
ufw allow 'Nginx Full' >/dev/null
ufw --force enable >/dev/null

# Har 10 daqiqada GitHub'dan yangilanadi: git push qilingan narsa o'zi saytga tushadi
cat > /etc/cron.d/agrosan-deploy <<'EOF'
*/10 * * * * root git -C /var/www/agrosan pull -q --ff-only
EOF

echo "TAYYOR: $(git -C /var/www/agrosan log --oneline -1)"
