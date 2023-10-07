about = "bruteforcing webcams by http/https"

class Main:
    def __init__(self):
        self.running = True
        self.ip_ranges = []
        
    def run(self):
        while self.running:
            command = input("IpCams>> ")
            command = command.split(" ")
            
            if command[0] == "set":
                match (command[1]):
                    case "ip_ranges":
                        self.ip_ranges = command[1].split(",")
            
            if command[0] == "show":
                pass
            if command[0] == "run":
                pass
    def exploit_start(self):
        pass
     
    def scan_range(self):
        pass