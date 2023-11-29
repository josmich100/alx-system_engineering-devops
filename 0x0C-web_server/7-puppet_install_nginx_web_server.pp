# Update package list
exec { 'update_package_list':
  command => 'apt-get -y update',
  path    => ['/usr/bin', '/usr/sbin', '/bin'],
}

# Install Nginx package
package { 'nginx':
  ensure => installed,
  require => Exec['update_package_list'],
}

# Allow Nginx HTTP in UFW
exec { 'allow_nginx_http':
  command => 'ufw allow \'Nginx HTTP\'',
  path    => ['/usr/bin', '/usr/sbin', '/bin'],
  require => Package['nginx'],
}

# Create default web page
file { '/var/www/html/index.nginx-debian.html':
  content => 'Hello World!',
  require => Package['nginx'],
}

# Set up redirection from /redirect_me to a YouTube link
exec { 'setup_redirection':
  command => "sed -i '/listen 80 default_server/a rewrite ^/redirect_me https://www.youtube.com/watch?v=bm9oGxhtbic&list=RDsJEoCE0QYYo&index=15 permanent;' /etc/nginx/sites-available/default",
  path    => ['/usr/bin', '/usr/sbin', '/bin'],
  require => Package['nginx'],
}

# Create custom 404 page
file { '/usr/share/nginx/html/custom_404.html':
  content => "Ceci n'est pas une page",
  require => Package['nginx'],
}

# Configure Nginx to use custom 404 page
exec { 'configure_custom_404':
  command => "sed -i '/listen 80 default_server/a error_page 404 /custom_404.html; location = /custom_404.html {root /usr/share/nginx/html; internal;}' /etc/nginx/sites-available/default",
  path    => ['/usr/bin', '/usr/sbin', '/bin'],
  require => Package['nginx'],
}

# Start Nginx service
service { 'nginx':
  ensure => running,
  enable => true,
  require => [
    Package['nginx'],
    File['/var/www/html/index.nginx-debian.html'],
    Exec['setup_redirection'],
    File['/usr/share/nginx/html/custom_404.html'],
    Exec['configure_custom_404'],
  ],
}
