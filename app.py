import sys
import nmap

def handler(event, context):
    host = event["host"]
    ports = ','.join([str(port) for port in event["ports"]])
    scanner = nmap.PortScanner()
    return scanner.scan(host, ports)
