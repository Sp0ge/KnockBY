import requests
import json

about = "Find open proxy in internet"
class main(object):
    def __init__(self):
        self.proxy
    
    def run(self):
        while self.running:
            command = input("$[ ProxyFinder ]>> ")
            command = command.split(" ")
            
    def proxy_check(ip: str):
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
        else:
            status["ip"] = f"{ip}"
        
        print(status)


