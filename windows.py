from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import subprocess
import socket
from text import MainWindow  # text.py에서 MainWindow 클래스 가져오기
import server
import client

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
port = 6112

class SignalHandler(QObject):
    received_signal = pyqtSignal(str)

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.processed_messages = set()  # 처리된 메시지 기록용 집합
        self.setWindowTitle("연결 프로그램")
        screen = self.screen().availableGeometry()
        self.resize(screen.width(), screen.height())
        self.showMaximized()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.is_server = False  # 서버인지 여부 확인
        self.client_connected = False  # 클라이언트가 접속했는지 여부 확인
        self.initUI()
    
    def initUI(self):
        self.select_layout = QVBoxLayout()
        self.create_btn = QPushButton('방 만들기')
        self.create_btn.clicked.connect(self.openServer)
        self.join_btn = QPushButton('방 참가')
        self.join_btn.clicked.connect(self.openClient)
        self.select_layout.addWidget(self.create_btn)
        self.select_layout.addWidget(self.join_btn)
        self.layout.addLayout(self.select_layout)

    def openServer(self):
        # 초기 선택 버튼 숨기기
        self.hideInitialButtons()
        self.is_server = True

        # 서버 소켓 초기화
        try:
            print("서버 소켓 초기화 중...")
            self.s = server.ServerSocket(self)
            self.s.update_signal.connect(self.clientStatusChanged)
            self.s.recv_signal.connect(self.updateMsg)
            print("서버 소켓 초기화 성공!")
        except Exception as e:
            print(f"서버 소켓 초기화 에러: {e}")
            return

        # 서버 UI 설정
        self.setWindowTitle('서버')
        ipbox = QHBoxLayout()
        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        box = QHBoxLayout()
        label = QLabel('Server IP')
        self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)

        self.btn = QPushButton('서버 실행')
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.toggleServer)
        box.addWidget(self.btn)

        gb.setLayout(box)
        self.layout.addLayout(ipbox)

        # 접속자 정보 표시를 위한 QTableWidget 추가
        self.guest_list = QTableWidget()
        self.guest_list.setColumnCount(2)
        self.guest_list.setHorizontalHeaderItem(0, QTableWidgetItem('IP'))
        self.guest_list.setHorizontalHeaderItem(1, QTableWidgetItem('Port'))
        self.layout.addWidget(QLabel("접속한 유저 목록"))
        self.layout.addWidget(self.guest_list)

        # 화면 열기 버튼
        self.open_screen_btn = QPushButton('화면 열기')
        self.open_screen_btn.setEnabled(False)  # 처음에는 비활성화
        self.open_screen_btn.clicked.connect(self.openTextWindow)
        self.layout.addWidget(self.open_screen_btn)

        self.show()

    def toggleServer(self):
        """서버 실행과 종료 상태를 전환하는 메서드"""
        if self.btn.isChecked():
            ip = self.ip.text()
            port = int(self.port.text())
            if self.s.start(ip, port):
                print("서버가 실행되었습니다.")
                self.btn.setText("서버 종료")
            else:
                print("서버 실행에 실패했습니다.")
                self.btn.setChecked(False)
        else:
            self.s.stop()
            print("서버가 종료되었습니다.")
            self.btn.setText("서버 실행")

    def openClient(self):
        # 초기 선택 버튼 숨기기
        self.hideInitialButtons()
        self.is_server = False

        # 클라이언트 소켓 초기화
        try:
            print("클라이언트 소켓 초기화 중...")
            self.c = client.ClientSocket(self)
            self.c.recv.recv_signal.connect(self.handleServerMessage)
            self.c.disconn.disconn_signal.connect(self.updateDisconnect)
            print("클라이언트 소켓 초기화 성공!")
        except Exception as e:
            print(f"클라이언트 소켓 초기화 에러: {e}")
            return

        # 클라이언트 UI 설정
        self.setWindowTitle('클라이언트')
        ipbox = QHBoxLayout()
        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        box = QHBoxLayout()
        label = QLabel('Server IP')
        self.ip = QLineEdit('172.30.1.27')
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit('6112')
        box.addWidget(label)
        box.addWidget(self.port)

        self.btn = QPushButton('접속')
        self.btn.clicked.connect(self.connectToServer)
        box.addWidget(self.btn)

        gb.setLayout(box)
        self.layout.addLayout(ipbox)

        # 화면 열기 버튼 (클라이언트는 자동으로 창을 열기 때문에 버튼을 숨깁니다)
        self.open_screen_btn = QPushButton('화면 열기')
        self.open_screen_btn.setVisible(False)  # 클라이언트에서는 숨김 처리
        self.layout.addWidget(self.open_screen_btn)

        self.show()

    def hideInitialButtons(self):
        """초기 선택 버튼을 숨기는 메서드"""
        self.create_btn.hide()
        self.join_btn.hide()

    def openTextWindow(self):
        """현재 ChatApp 레이아웃을 text.py의 MainWindow로 교체합니다."""
        self.clear_layout(self.layout)  # 기존 레이아웃 지우기
        self.main_window = MainWindow(self)  # text.py의 MainWindow 인스턴스 생성
        self.layout.addWidget(self.main_window)  # ChatApp에 MainWindow 추가
        self.setWindowTitle("밴픽 모드")  # 창 제목 변경
        if self.is_server:
            # 서버에서 버튼을 클릭하면 클라이언트에도 신호를 보냄
            self.s.send("open_window")

    def connectToServer(self):
        """클라이언트가 서버에 접속을 시도"""
        ip = self.ip.text()
        port = int(self.port.text())
        if self.c.connectServer(ip, port):
            self.btn.setText("접속 종료")
        else:
            self.btn.setText("접속")

    def clientStatusChanged(self, addr, is_connected):
        """서버에서 클라이언트 접속 상태 변경을 처리"""
        if self.is_server:
            if is_connected:
                row = self.guest_list.rowCount()
                self.guest_list.insertRow(row)
                self.guest_list.setItem(row, 0, QTableWidgetItem(addr[0]))
                self.guest_list.setItem(row, 1, QTableWidgetItem(str(addr[1])))
            else:
                for row in range(self.guest_list.rowCount()):
                    if (self.guest_list.item(row, 0).text() == addr[0] and
                            self.guest_list.item(row, 1).text() == str(addr[1])):
                        self.guest_list.removeRow(row)
                        break
            self.client_connected = is_connected
            self.open_screen_btn.setEnabled(self.client_connected)

    def updateDisconnect(self):
        """클라이언트 연결이 끊어졌을 때 호출되는 메서드"""
        print("클라이언트 연결이 끊어졌습니다.")
        self.btn.setText('접속')

    def clear_layout(self, layout):
        """주어진 레이아웃에서 모든 위젯을 제거합니다."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()  # 위젯 삭제
                elif item.layout():
                    self.clear_layout(item.layout())  # 서브 레이아웃 재귀 삭제

    def updateMsg(self, msg):
        """서버나 클라이언트에서 받은 메시지를 처리하는 메서드"""
            # 이미 처리된 메시지인지 확인
        if msg in self.processed_messages:
            return  # 이미 처리된 메시지라면 무시

        # 새 메시지라면 처리 후 기록
        self.processed_messages.add(msg)
        print(f"수신한 메시지: {msg}")
        if msg == "show_ban_team_selection":
            self.main_window.show_ban_team_selection()
        elif msg == "show_normal_team_selection":
            self.main_window.show_normal_team_selection()
        elif msg == "select_first_ban_team1":
            self.main_window.select_first_ban_team1()
        elif msg == "select_first_ban_team2":
            self.main_window.select_first_ban_team2()
        elif msg == "select_first_normal_team1":
            self.main_window.select_first_normal_team1()
        elif msg == "select_first_normal_team2":
            self.main_window.select_first_normal_team2()
        elif "select_character" in msg:
            character_name = msg.split(":")[1]
            character = next((c for c in self.main_window.characters if c["name"] == character_name), None)
            if character:
                self.main_window.select_character(character, self.main_window.character_buttons[character_name])
        elif "select_ban_character" in msg:
            character_name = msg.split(":")[1]
            character = next((c for c in self.main_window.characters if c["name"] == character_name), None)
            if character:
                self.main_window.select_ban_character(character, self.main_window.character_buttons[character_name], "ban")

    def handleServerMessage(self, msg):
        """클라이언트가 서버로부터 받은 메시지 처리"""
        if msg == "open_window":
            self.openTextWindow()
    
    def send_btn(self, text):
        """서버나 클라이언트로 start_ban_mode 신호를 보냅니다."""
        if text == "show_ban_team_selection":
            if self.is_server:
                self.s.send("show_ban_team_selection")  # 클라이언트에게 명령 전송
            else:
                self.c.send("show_ban_team_selection")  # 서버에게 명령 전송
        elif text == "show_normal_team_selection":
            if self.is_server:
                self.s.send("show_normal_team_selection")  # 클라이언트에게 명령 전송
            else:
                self.c.send("show_normal_team_selection")  # 서버에게 명령 전송
        elif text == "select_first_ban_team1":
            if self.is_server:
                self.s.send("select_first_ban_team1")  # 클라이언트에게 명령 전송
            else:
                self.c.send("select_first_ban_team1")  # 서버에게 명령 전송
        elif text == "select_first_ban_team2":
            if self.is_server:
                self.s.send("select_first_ban_team2")  # 클라이언트에게 명령 전송
            else:
                self.c.send("select_first_ban_team2")  # 서버에게 명령 전송
        elif text == "select_first_normal_team1":
            if self.is_server:
                self.s.send("select_first_normal_team1")  # 클라이언트에게 명령 전송
            else:
                self.c.send("select_first_normal_team1")  # 서버에게 명령 전송
        elif text == "select_first_normal_team2":
            if self.is_server:
                self.s.send("select_first_normal_team2")  # 클라이언트에게 명령 전송
            else:
                self.c.send("select_first_normal_team2")  # 서버에게 명령 전송
        elif "select_character" in text:
            character_name = text.split(":")[1]  # 캐릭터 이름을 추출
            if self.is_server:
                self.s.send(f"select_character:{character_name}")  # 클라이언트에 신호 전송
            else:
                self.c.send(f"select_character:{character_name}")  # 서버에 신호 전송
        elif "select_ban_character" in text:
            character_name = text.split(":")[1]  # 캐릭터 이름을 추출
            if self.is_server:
                self.s.send(f"select_ban_character:{character_name}")  # 클라이언트에 신호 전송
            else:
                self.c.send(f"select_ban_character:{character_name}")  # 서버에 신호 전송
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
