import sys
from tabulate import tabulate
import bluetooth

about = "Bluetooth hacking ToolKit"
class main(object):
    def __init__(self):
        self.devices = list()
        self.running = True
    
    def run(self):
        while self.running:
            try:
                command = input("$[Bluetooth]>> ")
                command = command.split(" ")
        
                if command[0] == "scan":
                    self.scan_devices()
                    
                elif command[0] == "help":
                    self.help()
                elif command[0] == "quit" or command[0] == "exit":
                    self.running = False
                else:
                    print("[no such command]")
                    
            except Exception as e:
                if "--debug" in sys.argv:
                        print(e.with_traceback(e))
                else:
                    print('[ Error ]')
    
    
    def help(self):
        help = [
            ["Commands","Description"],
            ["scan","scan for bluetooth devices"],
        ]
        print(tabulate(help, tablefmt="simple_grid"))
    
        
    def scan_devices(self):
        try:
            result = []
            discovered_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True,duration=4)
            print('Scanning for active devices...')
            print(f"Found {len(discovered_devices)} Devices\n")
            result.append(['Name','Address','Class'])
            for addr, name, device_class in discovered_devices:
                result.append([name,addr,device_class])
            self.devices = result
            print(tabulate(result, tablefmt="simple_grid"))
        except Exception as e:
            if "--debug" in sys.argv:
                    print(e.with_traceback(e))
            else:
                print('[ Error ]')
                
    def connect(self, a):
        pass