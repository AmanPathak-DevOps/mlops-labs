#!/bin/bash

set -e

# Installing/Updating the Packages
# Cloning the repo
# Creating and activating the Python virtual env
# Installing the dependency using requirements.txt
# Training the model
# Configuring the WSGI systemd service
# Configuring the NGINX systemd service
# Enabling the services to run at boot time

export WORK_DIR=/home/ubuntu/intent-app
mkdir -p $WORK_DIR
cd $WORK_DIR

apt update -y
apt install -y git python3 python3-venv python3-pip nginx

git clone https://github.com/AmanPathak-DevOps/mlops-labs.git

python3 -m venv .venv
source .venv/bin/activate

cd mlops-labs/intent-classifier-model-deploy-virtual-machine

python3 -m pip install -r requirements.txt

python3 model/train.py

cat >/etc/systemd/system/intent_gunicorn.service <<'EOF'
[Unit]
Description=Gunicorn instance for Intent Classifier
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/intent-app
Environment="PATH=/home/ubuntu/intent-app/.venv/bin"
ExecStart=/home/ubuntu/intent-app/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat >/etc/nginx/conf.d/intent_app.conf <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000/predict;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
    }
}
EOF

# Remove default site if present to avoid duplicate default_server collision
if [ -L /etc/nginx/sites-enabled/default ] || [ -f /etc/nginx/sites-enabled/default ]; then
  rm -f /etc/nginx/sites-enabled/default || true
fi

# start & enable services
systemctl daemon-reload
systemctl enable intent_gunicorn
systemctl start intent_gunicorn
systemctl enable nginx
systemctl restart nginx
