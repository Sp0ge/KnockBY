from scanners import net_scanner
import sys
class Switch:
    def switch_main(self, command):
        command = command.split(" ")
        match command[0]:
            case "net_scan":
                try:
                    net_scanner().discover(self.ip[int(command[1])], command[2])
                except Exception as e:
                    if "--debug" in sys.argv:
                        print(e.with_traceback())
                    else:     
                        self.main_menu("\n Require 2 args (net_scan [lan] [ports]) \n net_scan 0 80,443,22 \n")
                        
            case "port_scan":
                try:
                    net_scanner().port_scan(command[1])
                except Exception as e:
                    if "--debug" in sys.argv:
                        print(e.with_traceback())
                    else:     
                        self.main_menu("\n Require 1 args (port_scan [ip]) \n port_scan 127.0.0.1 \n")