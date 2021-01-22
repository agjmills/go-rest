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

        for protocol in scanner[host].all_protocols():
            ports_found = scanner[host][protocol].keys()
            for port in sorted(ports_found):
                newPort = Port(protocol, port, scanner[host][protocol][port]['state'])
                newHost.addPort(newPort)
        hosts.append(newHost.toJson())
    return hosts


class Host():
    def __init__(self, host, hostname, state):
        self.host = host
        self.hostname = hostname
        self.state = state
        self.ports = []

    def addPort(self, port):
        self.ports.append(port)

    def toJson(self):
        return {
            'host': self.host,
            'hostname': self.hostname,
            'state': self.state,
            'ports': list(map(lambda port: port.toJson(), self.ports))
        }


class Port():
    def __init__(self, protocol, port, state):
        self.protocol = protocol
        self.port = port
        self.state = state

    def toJson(self):
        return {
            "protocol": self.protocol,
            "port": self.port,
            "state": self.state
        }
