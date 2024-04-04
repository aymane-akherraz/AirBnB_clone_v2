#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static
apt-get -y update > /dev/null
apt-get -y upgrade > /dev/null
apt-get -y install nginx > /dev/null
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -hR ubuntu:ubuntu /data
sudo sed -i '/server_name _;/a\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default
service nginx restart
