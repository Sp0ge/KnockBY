import uuid
import socket
import tabulate

class NetworkTools:
    def __init__(self):
        self.mac = self.get_mac()
        self.ip = self.get_ip()
        self.hostname = self.get_hostname()
            
    def get_mac(self):
        return str(':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]))
        
    def get_ip(self):
        return socket.gethostbyname_ex(socket.gethostname())[-1]
    
    def get_hostname(self):
        return socket.getfqdn()
    
    def get_network_table(self, args):
        table = []
        headers = []
        for arg in args:
            
            if arg == "ip":
                
                for num, ip in enumerate(self.get_ip()):
                    headers.append(f"IP|LAN{num}")
                    table.append(ip)
                    
            if arg == "mac":
                
                headers.append("MAC_Address")
                table.append(self.mac)
                
            if arg == "hostname":
                
                headers.append("Hostname")
                table.append(self.hostname)
            
        return tabulate.tabulate([table],headers ,tablefmt="simple_grid")