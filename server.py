from threading import Thread
from socket import *
from PyQt5.QtCore import pyqtSignal, QObject

class ServerSocket(QObject):
    update_signal = pyqtSignal(tuple, bool)  # 접속 상태 변경 시그널
    recv_signal = pyqtSignal(str)            # 메시지 수신 시그널
 
    def __init__(self, parent):        
        super().__init__()
        self.parent = parent
        self.bListen = False       
        self.clients = []
        self.ip = []
        self.threads = []
 
        self.update_signal.connect(self.parent.clientStatusChanged)
        self.recv_signal.connect(self.parent.updateMsg)
         
    def __del__(self):
        self.stop()
 
    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)            

        try:
            self.server.bind((ip, port))
        except Exception as e:
            return False
        else:                 
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
 
        return True
 
    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):            
            self.server.close()       
 
    def listen(self, server):
        while self.bListen:
            server.listen(5)   
            try:
                client, addr = server.accept()
            except Exception as e:
                break
            else:                
                self.clients.append(client)
                self.ip.append(addr)                
                self.update_signal.emit(addr, True)  # 접속 상태 업데이트                
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()                
                 
        self.removeAllClients()
        self.server.close()
 
    def receive(self, addr, client):
        while True:            
            try:
                recv = client.recv(1024)                
            except Exception as e:   
                print('[ERROR] Recv() Error:', e)        
                break
            else:                
                msg = str(recv, encoding='utf-8')
                if msg:
                    print(f"[DEBUG] Received message from {addr}: {msg}")  # 수신 성공 로그
                    self.handle_message(addr, msg)
 
        self.removeClient(addr, client)

    def handle_message(self, addr, msg):
        """받은 메시지를 처리하고 필요한 경우 전송"""
        if msg.startswith("button_click"):
            print(f"[DEBUG] Broadcasting button click event: {msg}")  # 브로드캐스트 로그
            self.send(msg)
        else:
            self.recv_signal.emit(msg)

    def send(self, msg):
        """모든 클라이언트에 메시지 전송"""
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)
 
    def removeClient(self, addr, client):
        """클라이언트가 연결 해제되었을 때 처리"""
        idx = -1
        for k, v in enumerate(self.clients):
            if v == client:
                idx = k
                break

        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        del self.threads[idx]
        self.update_signal.emit(addr, False)  # 접속 해제 상태 업데이트