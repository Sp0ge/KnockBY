import requests
from threading import Thread
import json
import sys

about = "Find open proxy in internet"
class main(object):
    def __init__(self):
        self.proxy_list = list()
        self.good_proxy = list()
        self.running = True
    
    def run(self):
        while self.running:
            try:
                command = input("$[ProxyFinder]>> ")
                command = command.split(" ")
        
                if command[0] == "set":
                    if command[1] == "proxy_list":
                        self.proxy_list = list(command[2].split(","))
                    else:
                        print("[no such argument for get]")
                
                elif command[0] == "get":
                    if command[1] == "proxy_list":
                        print(self.proxy_list)
                    elif command[1] == "good_proxy":
                        for proxy_data in self.good_proxy:
                            print(f"{proxy_data['ip']} \t\t code: {proxy_data['status_code']} \t response_time: {proxy_data['response_time']}")
                    
                    else:
                        print("[no such argument for get]")
                elif command[0] == "checkproxy":
                    self.proxy_check(command[1])
                    
                elif command[0] == "masscheck":
                    self.massproxycheck()
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
        print("""
set - input options [proxy_list]
get - get info of [proxy_list, good_proxy]          

checkproxy - checking if proxy is online and type of [http / https]
masscheck  - checking all proxy in list if online and type of [http / https]
              """)
            
    def massproxycheck(self):
        threads = []
        
        for ip in self.proxy_list:
            threads.append(Thread(target=self.proxy_check, args=[str(ip)]))
            
        for worker in threads:
            worker.start()
        
        for worker in threads:
            worker.join()

            
    def proxy_check(self, ip: str):
        status = {
            "ip":None,
            "online":False,
            "status_code":None,
            "protocol":None,
            "response_time":None
        }
        
        
        try:
            proxy = {
                "https":f'{ip}:443'
            }
            
            answer = requests.get(
                url='https://google.com',
                proxies=proxy
                )
            status["protocol"] = "https"
        except Exception as e:
            pass
            
        try:
            proxy = {
                "http":f'{ip}:443'
            }
            answer = requests.get(
                url='http://google.com',
                proxies=proxy
                )
            status["protocol"] = "http"
        except Exception as e:
            pass
    
    
        if status["protocol"] is not None:
            status["online"] = True
            status["ip"] = f"{status['protocol']}://{ip}"
            status["response_time"] = answer.elapsed.total_seconds()
            status["status_code"] = answer.status_code
            self.good_proxy.append(status)
        else:
            status["ip"] = f"{ip}"
             
        print(json.dumps(status, indent=4))