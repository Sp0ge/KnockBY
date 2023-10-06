from network import NetworkTools
from tunnel import Switch
import os
import tabulate
import sys

class MainUtilMenu(NetworkTools, Switch):
    def __init__(self):
        NetworkTools.__init__(self)
        Switch.__init__(self)
        self.running = True
        
    def run(self):
        self.clear_terminal
        self.main_menu()

    def main_menu(self, warning=None):
        print(self.get_network_table(["ip","mac","hostname"]), end="\n\r")
        self.clear_terminal()
        print(self.get_network_table(["ip","mac","hostname"]), end="\n\r")
        while self.running:
            if warning is not None:
                print(f"\n Warning - [ {warning} ] \n")
            command = input(f"{str(self.hostname)}>>")
            if command == "quit": self.quit()
            if command == "help": self.help()
            if command == "clear": self.clear_terminal()
            self.switch_main(command)
    def clear_terminal(self):
        os.system("cls||clear")
    
    def quit(self):
        self.clear_terminal()
        if input(f"QUIT? y/N >>").lower() == "y":
            sys.exit(0)
        else:
            self.main_menu()
        
    
    def help(self):
        
        help=[
            ["help","show this menu"],
            ["net_scan [lan] [port]", "discovering all devices in local network and open port on it"],
            ["port_scan [ip]", "discovering all open ports on target"],
            ["quit", "close menu"],
            
        ]
            
        print(tabulate.tabulate(help, tablefmt="simple_grid"))
    
if __name__ == "__main__":
    if "--debug" in sys.argv:
        MainUtilMenu().run()
    else:
        try:  
            MainUtilMenu().run()
        except Exception as e:
            print("You catch Fatal error!")