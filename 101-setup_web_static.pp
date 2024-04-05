# Sets up your web servers for the deployment of web_static

package { 'nginx':
  ensure => installed,
}

exec {'test folder':
  command => '/usr/bin/env mkdir -p /data/web_static/releases/test/',
}
exec {'shared folder':
  command => '/usr/bin/env mkdir -p /data/web_static/shared/',
}
exec {'chown:':
  command => '/usr/bin/env chown -R ubuntu:ubuntu /data',
}
file { '/data/web_static/releases/test/index.html':
  content => "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>",
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

file_line { 'adding config':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  line   => "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
  after  => 'server_name _;',
}

service { 'nginx':
  ensure  => running,
  restart => true,
}
