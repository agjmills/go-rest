import nmap

def handler(event, context):
    host = event["host"]
    ports = ','.join([str(port) for port in event["ports"]])

    return scan(host, ports)

def scan(host, ports):
    scanner = nmap.PortScanner()
    scanner.scan(host, ports)

    hosts = []
    for host in scanner.all_hosts():
        newHost = Host(host, scanner[host].hostname(), scanner[host].state())

        for proto in scanner[host].all_protocols():
            lport = scanner[host][proto].keys()
            lport.sort()
            for port in lport:
                newPort = Port(proto, port, scanner[host][proto][port]['state'])
                newHost.addPort(newPort)
        hosts.append(newHost)
    return hosts

class Host:
    def __init__(self, host, hostname, state):
        self.host = host
        self.hostname = hostname
        self.state = state
        self.ports = []

    def addPort(self, port):
        self.ports.append(port)

class Port:
    def __init__(self, protocol, port, state):
        self.protocol = protocol
        self.port = port
        self.state = state