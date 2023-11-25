# using puppet to kill a process
exec {'killmenow':
    command => 'pkill killmenow',
    path => '/usr/bin'
}
