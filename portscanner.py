#!/usr/bin/env python3

import socket
import time
import yaml
import os
import sys
import json
import logging
import argparse
from prometheus_client import start_http_server, Gauge

# Set up logging
logging.basicConfig(level=logging.INFO, format='{ "date_time": "%(asctime)s", "loglevel": "%(levelname)s", "message": %(message)s}', handlers=[logging.StreamHandler()])
logger = logging.getLogger()

# Generate example config file
def generate_config():
    data = """#Simple configuration
logging: true
timeout: 1
hosts:
  - host: "localhost"
    ports: [80, 443, 22, 28882]
    protocol: "tcp"
    check_interval: 10
  - host: "exampleasdsad.com"
    ports: [80, 443, 21]
    protocol: "tcp"
    check_interval: 15
  - host: "192.168.20.1"
    ports: [53, 67, 68]
    protocol: "udp"
    check_interval: 20
    """
    with open('config.yaml', 'w') as file:
        file.write(data)    

# Load configuration from YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to scan ports
def scan_ports(host, ports, protocol, logging, timeout):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((host, port))
            if logging:
                logger.info(json.dumps({"host": host, "port": port, "protocol": protocol, "status": "open"}))
            if result == 0:
                open_ports.append(port)
        except Exception:
            if logging:
                logger.info(json.dumps({"host": host, "port": port, "protocol": protocol, "status": "closed or host unknown"}))
        sock.close()
    return open_ports

# Main function
def main():
    parser = argparse.ArgumentParser(description='Simple port scanner.')
    parser.add_argument("command", help="run - run command, generate - generate and override config.yaml file")
    parser.add_argument("--port", action="store_true", help="Change default (tcp/8000) http port.")
    parser.add_argument("--config", action="store_true", help="Change default config file path. File in yaml format")
    parser.add_argument("--node", action="store_true", help="Hostname from generated node, support ENV.NODE too. If not defined use hostname")

    args = parser.parse_args()

 
    host_from = os.environ.get('NODE', socket.gethostname())
    http_port = args.port if args.port else 8000
    config_file = args.config if args.config else "config.yaml"
    
    if args.node:
        host_from = args.node
    
    if args.command == "run":
        logger.info('"Run service"')
    elif args.command == "generate":
        logger.info('"Generate config in config.yaml file"')
        generate_config()
        sys.exit()
    else:
        sys.exit("Invalid command. Use 'run' or 'generate'.")
    
    config = load_config(config_file)
    start_http_server(http_port)
    
    gauges = {}
    
    gauges[host_from] = Gauge('portscan', 'Open ports for host', ['source_host', 'remote_host','port', 'protocol'])
    
    while True:
        for host in config['hosts']:
            open_ports = scan_ports(host['host'], host['ports'], host['protocol'], config['logging'], config['timeout'])
            for port in open_ports:
                gauges[host_from].labels(source_host=host_from, remote_host=host['host'], port=port, protocol=host['protocol']).set(1)
            time.sleep(host['check_interval'])

if __name__ == "__main__":
    main()
