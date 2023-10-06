import socket
import tqdm
import tabulate
import threading
import os
import time

class net_scanner:
    def discover(self, network, ports):
        net = network.split(".")
        result = []
        threads = []
        for i in range(1, 256):
            net[3] = str(i)
            ip = ".".join(net)
            for port in ports.split(","):
                threads.append(threading.Thread(target=self.ports_check, args=(ip, int(port), result)))
                
        for thread in threads:
            thread.start()
            
        
        for thread in tqdm.tqdm(range(0,len(threads))):
            threads[thread].join()
        os.system("cls||clear")
        if len(result) < 1:
            print("\n [ Nothing found ] \n")
            
        else:
            print(tabulate.tabulate(result, headers=["IP","PORT"], tablefmt="simple_grid"))
        
    def ports_check(self,ip, port, result):
        target = socket.gethostbyname(ip)
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ans = s.connect_ex((target,port))
        s.close()
        if ans == 0:
            result.append([ip, port])
    
    def port_check(self,ip, port, result):
        target = socket.gethostbyname(ip)
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ans = s.connect_ex((target,port))
        s.close()
        if ans == 0:
            result.append([port])
            
    def port_scan(self, ip):
        result = []
        threads = []
        for port in range(0,65536):
            threads.append(threading.Thread(target=self.port_check, args=(ip, int(port), result)))
                
        for thread in tqdm.tqdm(range(0,len(threads), 4096)):
            for part in range(4096):
                if (thread+part) < 65536:
                    threads[thread+part].start()
            for part in range(4096):
                if (thread+part) < 65536:
                    threads[thread+part].join()

        if len(result) < 1:
            print("\n [ Nothing found ] \n")    
        else:
            print(tabulate.tabulate(result, headers=["PORT"], tablefmt="simple_grid"))