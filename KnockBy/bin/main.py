from bin.network import NetworkTools
from bin.tunnel import Switch
import os
import tabulate

class MainUtilMenu(NetworkTools, Switch):
    def __init__(self):
        NetworkTools.__init__(self)
        Switch.__init__(self)
        self.running = True
        
    def run(self):
        self.clear_terminal
        self.main_menu()

    def main_menu(self, warning=None):
        self.clear_terminal()
        print(self.get_network_table(["ip","mac","hostname"]), end="\n\r")
        while self.running:
            if warning is not None:
                print(f"\n Warning - [ {warning} ] \n")
                warning = None
            command = input(f"$[KnockBy]~{str(self.hostname)}>>")
            if command == "quit" or command == "exit":
                self.quit()
            elif command == "help":
                self.help()
            elif command == "clear":
                self.clear_terminal()
            else:
                self.switch_main(command)
            
    def clear_terminal(self):
        os.system("cls||clear")
        print(self.get_network_table(["ip","mac","hostname"]), end="\n\r")
    
    def quit(self):
        self.clear_terminal()
        if input("QUIT? y/N >>").lower() == "y":
            self.running = False
        else:
            self.main_menu()
        
    
    def help(self):
        
        help=[
            ["help","show this menu"],
            ["net_scan [lan] [port]", "discovering all devices in local network and open port on it"],
            ["port_scan [ip]", "discovering all open ports on target"],
            ["use [tool]", "enter tool to use"],
            ["show", "show tools"],
            ["quit", "close menu"],
            
        ]
            
        print(tabulate.tabulate(help, tablefmt="simple_grid"))
