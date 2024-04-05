# Sets up your web servers for the deployment of web_static

package { 'nginx':
  ensure => installed,
}

file { ['/data',
  '/data/web_static',
  '/data/web_static/releases',
  '/data/web_static/shared',
  '/data/web_static/releases/test', ]:
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  mode    => '0755',
}

file { '/data/web_static/releases/test/index.html':
  content => "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>",
}

file_line { '':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  line   => 'location /hbnb_static/ {
                alias /data/web_static/current/;
                autoindex off;
            }',
  after  => 'server_name _;',
}

service { 'nginx':
  ensure  => running,
  restart => true,
}
