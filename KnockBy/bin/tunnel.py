from bin.scanners import net_scanner
import sys
import os
import tabulate
import traceback

BASE_DIR = os.getcwd()

class Switch:
    def switch_main(self, command):
        command = command.split(" ")
        match command[0]:
            case "net_scan":
                try:
                    net_scanner().discover(self.ip[int(command[1])], command[2])
                except Exception as e:
                    if "--debug" in sys.argv:
                        print(traceback.format_exc())
                    else:     
                        self.main_menu("\n Require 2 args (net_scan [lan] [ports]) \n net_scan 0 80,443,22 \n")
                    
            case "port_scan":
                try:
                    net_scanner().port_scan(command[1])
                except Exception as e:
                    if "--debug" in sys.argv:
                        print(traceback.format_exc())
                    else:     
                        self.main_menu("\n Require 1 args (port_scan [ip]) \n port_scan 127.0.0.1 \n")
                        
            case "show":
                table = []
                for tool in os.listdir(os.path.join(BASE_DIR, os.path.normpath("tools"))):
                    if ".py" in tool:  
                        tool = tool.replace(".py","")
                        try:
                            mod = __import__(f"tools.{tool}", fromlist=["about"])
                            table.append([tool,mod.about])
                        except Exception as e:
                            if "--debug" in sys.argv:
                                print(traceback.format_exc())
                            else: 
                                print(f"[ {tool} load Fail ]", end="\n")                             
                print(tabulate.tabulate(table, headers=["Tool","Description"], tablefmt="simple_grid"))
                    
            case "use":
                try:
                    tool = __import__(f"tools.{str(command[1])}", fromlist=["main"])
                    tool.main().run()
                except Exception as e:
                    if "--debug" in sys.argv:
                        print(e)
                    else:     
                        self.main_menu("\n[ Module fatal error ]\n")
            case _:
                print("[ no such command ]")
            
    def tool_select(self,tool):
        pass