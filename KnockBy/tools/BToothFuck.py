import bluetooth
import sys

from pathlib import Path

about = "Bluetooth hacking ToolKit"
class main(object):
    def __init__(self):
        self.running = True
    
    def run(self):
        while self.running:
            try:
                command = input("$[ProxyFinder]>> ")
                command = command.split(" ")
            
            
            except Exception as e:
                if "--debug" in sys.argv:
                        print(e.with_traceback(e))
                else:
                    print('[ Error ]')