#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R root:root /data/

# Update Nginx configuration
config="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "/server_name _;/a $config" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
