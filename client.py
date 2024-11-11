from threading import Thread
from socket import *
from PyQt5.QtCore import pyqtSignal, QObject

class Signal(QObject):  
    recv_signal = pyqtSignal(str)
    disconn_signal = pyqtSignal()   

class ClientSocket:
    def __init__(self, parent=None):        
        self.parent = parent                
        
        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateMsg)  # updateMsg 연결
        self.bConnect = False

        self.disconn = Signal()
        self.disconn.disconn_signal.connect(self.parent.updateDisconnect)
 
    def connectServer(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)           
        try:
            self.client.connect((ip, port))
        except Exception as e:
            print('Connect Error:', e)
            return False
        else:
            self.bConnect = True
            self.t = Thread(target=self.receive, args=(self.client,))
            self.t.start()
            print('Connected')
        return True
 
    def stop(self):
        self.bConnect = False       
        if hasattr(self, 'client'):            
            self.client.close()
            del self.client
            self.disconn.disconn_signal.emit()
 
    def receive(self, client):
        while self.bConnect:            
            try:
                recv = client.recv(1024)                
            except Exception as e:              
                break
            else:                
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.recv.recv_signal.emit(msg)
                    print(f"[DEBUG] Message received in ClientSocket: {msg}")
        self.stop()
 
    def send(self, msg):
        if not self.bConnect:
            print("[DEBUG] Client not connected, unable to send message.")
            return

        try:            
            self.client.send(msg.encode())
            print(f"[DEBUG] Message sent to server: {msg}")  # 전송 성공 로그
        except Exception as e:
            print('Send() Error : ', e)

    def send_button_click(self, button_id):
        """버튼 클릭 이벤트를 서버로 전송"""
        msg = f"button_click:{button_id}"
        self.send(msg)
