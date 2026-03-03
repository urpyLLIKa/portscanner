Simple python script for portscan and publish in prometheus format
need for k8s services

binary build - use nuitka


prometheus output
# HELP portscan Open ports for host
# TYPE portscan gauge
portscan{port="80",protocol="tcp",remote_host="localhost",source_host="debian"} 1.0
portscan{port="22",protocol="tcp",remote_host="localhost",source_host="debian"} 1.0


console log
{ "date_time": "2026-03-04 01:11:05,850", "loglevel": "INFO", "message": {"host": "192.168.20.1", "port": 53, "protocol": "udp", "status": "open"}}
{ "date_time": "2026-03-04 01:11:05,850", "loglevel": "INFO", "message": {"host": "192.168.20.1", "port": 67, "protocol": "udp", "status": "open"}}
{ "date_time": "2026-03-04 01:11:05,851", "loglevel": "INFO", "message": {"host": "192.168.20.1", "port": 68, "protocol": "udp", "status": "open"}}
