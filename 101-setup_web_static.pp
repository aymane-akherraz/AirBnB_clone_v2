# Sets up your web servers for the deployment of web_static

package { 'nginx':
  ensure => installed,
}

file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  mode    => '0755',
}

file { '/data/web_static':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  mode    => '0755',
}

file { '/data/web_static/releases':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  mode    => '0755',
}

file { '/data/web_static/shared':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  mode    => '0755',
}

file { '/data/web_static/releases/test':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  mode    => '0755',
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
