# 101-setup_web_static.pp

# Install Nginx
class { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html><head></head><body>Holberton School</body></html>',
  owner   => 'root',
  group   => 'root',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'root',
  group  => 'root',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => "
    server {
        listen 80 default_server;
        server_name _;

        location /hbnb_static {
            alias /data/web_static/current;
        }

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
  ",
  require => Class['nginx'],  # Add this line to ensure Nginx class is defined before this resource
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
