enable_all false

# Enable everything but MySQL
proxy[:enable] = true
memcached[:enable] = true
web[:enable] = true
rrd[:enable] = true
cron[:enable] = true
service[:enable] = true

app[:ip_ranges] = ['172.0.0.0/16']
app[:security_group_name] = 'scalrSecurityGroup'
supervisor[:tz] = 'Europe/Amsterdam'
routing[:endpoint_host] = 'scalrserver.poc.nl'

# Use separate MySQL
app[:mysql_scalr_host] = '127.0.0.1'      # Host for the Scalr MySQL database.
app[:mysql_scalr_port] = 3306             # Port for the Scalr MySQL database. (note that by default the installer sets up MySQL to listen on port 6280).

app[:mysql_analytics_host] = '127.0.0.1'  # Host for the Analytics MySQL database.
app[:mysql_analytics_port] = 3306         # Port for the Analytics MySQL database (same as above).

