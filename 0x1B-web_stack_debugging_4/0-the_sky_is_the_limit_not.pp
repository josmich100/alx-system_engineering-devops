# File: 0-the_sky_is_the_limit.pp

# Define an exec resource to run the ab command
exec { 'ab_benchmark':
  command     => '/usr/bin/ab -c 100 -n 2000 http://localhost/',
  logoutput   => true,
  refreshonly => true,
}

# Define the Nginx service
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Exec['ab_benchmark'],
}

# Define a file resource to manage the Nginx default configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => template('path/to/your/nginx_config.erb'), # You need to provide the correct path to your Nginx config template
  notify  => Service['nginx'],
}
