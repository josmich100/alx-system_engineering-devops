# 2-puppet_custom_http_response_header.pp

# Install Nginx
class {'nginx':
  ensure => 'installed',
}

# Custom HTTP header configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
}

# Nginx service management
service {'nginx':
  ensure => 'running',
  enable => true,
}

# Custom HTTP header template
file { '/etc/nginx/sites-available/default.erb':
  ensure => file,
  content => '# Custom HTTP header configuration\nserver {\n    listen 80 default_server;\n    listen [::]:80 default_server;\n\n    server_name _;\n\n    location / {\n        add_header X-Served-By $hostname;\n        root /var/www/html;\n        index index.html;\n    }\n\n    error_page 404 /404.html;\n    location = /404.html {\n        root /var/www/html;\n        internal;\n    }\n\n    error_page 500 502 503 504 /50x.html;\n    location = /50x.html {\n        root /var/www/html;\n        internal;\n    }\n}\n',
}

# Notify the custom template change
notify { 'nginx_custom_header':
  message => 'Nginx custom header configuration updated.',
  require => File['/etc/nginx/sites-available/default.erb'],
}
