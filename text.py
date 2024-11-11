from PyQt5.QtWidgets import QFrame, QGridLayout, QApplication, QMainWindow, QWidget, QLabel, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QSize, Qt, QCoreApplication, QTimer
import sys
import os
import pygame


class MainWindow(QMainWindow):
    def __init__(self, chat_app):
        super().__init__()
        # pygame 초기화
        pygame.mixer.init()
        self.chat_app = chat_app
        self.character_buttons = {}
        image_folder = self.resource_path("image")
        self.sound_path = self.resource_path("sound.mp3")
        self.siren_path = self.resource_path("siren.mp3")
        # 캐릭터 데이터 예시
        self.characters = []
        self.eternel_ban_characters = [
            "카구라자카 아스나", "양 샤오 롱", "아서스 메네실", "타카나시 호시노", "프레이 마이어", "가오가이가", "료 사카자키", "타카마치 나노하", "클레", "리바이 아커만"
        ]
        self.character_names = ["룰러", 
        "마샬 D 티치", 
        "아서스 메네실", 
        "도바킨", 
        "카구라자카 아스나", 
        "이츠카 코토리", 
        "사냥꾼", 
        "후지와라노 모코우", 
        "2B", 
        "캡틴 아메리카", 
        "양 샤오 롱", 
        "랄프 존스", 
        "레밀리아 스칼렛", 
        "페코린느", 
        "자이언트", 
        "타카나시 호시노", 
        "가면의 아이작", 
        "샤나", 
        "몽키 D. 루피", 
        "키리토", 
        "세이버", 
        "카네키 켄", 
        "콘파쿠 요우무", 
        "가츠", 
        "히메라기 유키나", 
        "시온 자일", 
        "쿠사나기 쿄", 
        "히나나위 텐시", 
        "아슈타르테", 
        "프레이 마이어", 
        "카마도 탄지로", 
        "크로노스", 
        "가오가이가", 
        "아리마 미야코", 
        "손오공", 
        "린네", 
        "료 사카자키", 
        "아쳐", 
        "북방서희", 
        "미사카 미코토", 
        "하쿠레이 레이무", 
        "파츄리 노우릿지", 
        "루이스", 
        "타카마치 나노하", 
        "리인포스", 
        "루비 로즈", 
        "리나 인버스", 
        "데스페라도", 
        "타츠마키", 
        "클레", 
        "시논", 
        "키리사메 마리사", 
        "서리별", 
        "로이 머스탱", 
        "아키타입 어스", 
        "아오자키 아오코", 
        "에드워드 엘릭", 
        "아크메이지", 
        "혜진", 
        "야보쿠", 
        "료우기 시키", 
        "토오노 시키", 
        "J 헤이스팅스", 
        "히무라 켄신", 
        "우치하 사스케", 
        "야가미 이오리", 
        "이사야마 요미", 
        "세이버 알터", 
        "어벤저", 
        "아카메", 
        "쿠로사키 이치고", 
        "겐지", 
        "소우게츠 유즈리하", 
        "라이덴 쇼군", 
        "아이하라 엔쥬", 
        "사토미 렌타로", 
        "우즈마키 나루토", 
        "늑대", 
        "조마에 사오리", 
        "루시아", 
        "리바이 아커만", 
        "사무엘 호드리게스", 
        "나가노하라 요이미야", 
        "스텔라", 
        "엑스", 
        "쿠마가와 미소기", 
        "해리 제임스 포터", 
        "Springfield M93", 
        "Drakedog", 
        "니케", 
        "유령", 
        "마르코 롯시", 
        "HK 46", 
        "콜 캐서디", 
        "키아나 카스라나", 
        "시라스 아즈사", 
        "티나 스프라우트", 
        "토키사키 쿠루미", 
        "스폰지밥", 
        "솔라", 
        "하츠네 미쿠", 
        "웨슬리 슬로언", 
        "마키세 크리스", 
        "아쿠아", 
        "시스티나 피벨", 
        "코메이지 코이시", 
        "여신관", 
        "호라이산 카구야", 
        "고토 히토리"]

        for i, name in enumerate(self.character_names, start=1):
            # 이미지 파일 이름 예시: 'ggg (1).png', 'ggg (2).png' 등
            image_path = os.path.join(image_folder, f"ggg ({i}).png")
            
            # 이미지 파일이 있으면 불러오고, 없으면 임시 이미지를 생성
            if os.path.exists(image_path):
                img = QPixmap(image_path)
            else:
                img = QPixmap(80, 80)
                img.fill(Qt.gray)  # 회색 임시 이미지로 설정
            
            # 캐릭터 데이터 추가
            self.characters.append({"name": name, "image": img})
        
        # 픽 순서 및 팀 초기 설정
        self.default_ban_order = [(1, "Team 1"), (2, "Team 2")] * 5
        self.alternate_ban_order = [(2, "Team 2"), (1, "Team 1")] * 5
        self.default_pick_order = [(1, "Team 1"), (2, "Team 2"), (2, "Team 2"), (1, "Team 1"), (1, "Team 1"), (2, "Team 2")]
        self.alternate_pick_order = [(2, "Team 2"), (1, "Team 1"), (1, "Team 1"), (2, "Team 2"), (2, "Team 2"), (1, "Team 1")]
        
        # 현재 선택된 픽/밴 정보 및 상태
        self.picks = {"Team 1": [], "Team 2": []}
        self.bans = {"Team 1": [], "Team 2": []}
        self.is_ban_phase = False  # 초기화 시 기본값 설정
        self.is_ban_phase2 = False  # 초기화 시 기본값 설정
        self.current_pick = 0
        self.current_ban = 0

        self.setWindowTitle("모드 선택")
        # 화면 크기 얻기
        screen = self.screen().availableGeometry()
        self.resize(screen.width(), screen.height())
        self.showMaximized()

        # 메인 위젯 및 레이아웃 설정
        self.main_widget = QWidget()
        layout = QVBoxLayout()
        self.main_widget.setLayout(layout)

        # 라벨
        label = QLabel("모드를 선택하세요")
        label.setStyleSheet("font-size: 16pt; font-family: Arial;")  # 폰트 크기 및 스타일 설정
        layout.addWidget(label)

        # 밴픽모드 버튼
        ban_pick_button = QPushButton("밴픽모드")
        ban_pick_button.setFixedSize(300, 50)
        ban_pick_button.clicked.connect(self.start_ban_mode)
        layout.addWidget(ban_pick_button)

        # 일반모드 버튼
        general_mode_button = QPushButton("일반모드")
        general_mode_button.setFixedSize(300, 50)
        general_mode_button.clicked.connect(self.start_normal_mode)
        layout.addWidget(general_mode_button)

        # 레이아웃을 메인 위젯에 설정하고 중앙에 배치
        self.main_widget.setLayout(layout)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setCentralWidget(self.main_widget)
    
    def resource_path(self, relative_path):
        """PyInstaller와 호환되는 리소스 경로 반환"""
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 빌드된 .exe 환경의 임시 폴더 경로
            return os.path.join(sys._MEIPASS, relative_path)
        # 개발 환경 (Python 스크립트 실행)에서의 경로
        return os.path.join(os.path.abspath("."), relative_path)

    # 밴 모드 시작 함수
    def start_ban_mode(self):
        self.chat_app.send_btn("show_ban_team_selection")
        self.show_ban_team_selection()

    # 노말 모드 시작 함수
    def start_normal_mode(self):
        self.chat_app.send_btn("show_normal_team_selection")
        self.show_normal_team_selection()

    def clear_layout(self, widget):
        layout = widget.layout()  # 위젯의 레이아웃을 가져옵니다.

        # 기존 레이아웃이 있는 경우 모든 위젯을 제거합니다.
        if layout is not None:
            while layout.count() > 0:
                child = layout.takeAt(0)  # 레이아웃에서 위젯을 제거
                if child.widget():  # 위젯이 있으면 삭제
                    child.widget().deleteLater()
                    
    def show_ban_team_selection(self):
        # 현재 레이아웃을 지우고 새로운 레이아웃 생성
        self.clear_layout(self.main_widget)
        
        # 라벨과 버튼 추가
        layout = self.main_widget.layout()  # 기존 레이아웃을 가져옵니다.
        label = QLabel("어떤 팀이 선픽인지 선택하세요")
        label.setStyleSheet("font-size: 16pt; font-family: Arial;")
        layout.addWidget(label)

        # 1팀 버튼
        team1_button = QPushButton("1팀")
        team1_button.setFixedSize(400, 50)
        team1_button.clicked.connect(lambda: (self.select_first_ban_team1(), self.chat_app.send_btn("select_first_ban_team1")))
        layout.addWidget(team1_button)

        # 2팀 버튼
        team2_button = QPushButton("2팀")
        team2_button.setFixedSize(400, 50)
        team2_button.clicked.connect(lambda: (self.select_first_ban_team2(), self.chat_app.send_btn("select_first_ban_team2")))
        layout.addWidget(team2_button)

    # 선픽 팀 선택 화면 표시 함수 (일반 모드)
    def show_normal_team_selection(self):
        # 현재 레이아웃을 지우고 새로운 레이아웃 생성
        self.clear_layout(self.main_widget)
        
        # 라벨과 버튼 추가
        layout = self.main_widget.layout()  # 기존 레이아웃을 가져옵니다.
        label = QLabel("어떤 팀이 선픽인지 선택하세요")
        label.setStyleSheet("font-size: 16pt; font-family: Arial;")
        layout.addWidget(label)

        # 1팀 버튼
        team1_button = QPushButton("1팀")
        team1_button.setFixedSize(400, 50)
        team1_button.clicked.connect(lambda: (self.select_first_normal_team1(), self.chat_app.send_btn("select_first_normal_team1")))
        layout.addWidget(team1_button)

        # 2팀 버튼
        team2_button = QPushButton("2팀")
        team2_button.setFixedSize(400, 50)
        team2_button.clicked.connect(lambda: (self.select_first_normal_team2(), self.chat_app.send_btn("select_first_normal_team2")))
        layout.addWidget(team2_button)
    
    # 선픽 팀 선택 함수 (밴 모드)
    def select_first_ban_team1(self):
        self.pick_order = self.default_pick_order
        self.ban_order = self.default_ban_order
        self.current_ban = 0

        self.clear_layout(self.main_widget)
        self.start_ban_pick_mode()
    
    # 선픽 팀 선택 함수 (밴 모드)
    def select_first_ban_team2(self):
        self.pick_order = self.alternate_pick_order
        self.ban_order = self.alternate_ban_order
        self.current_ban = 0

        self.clear_layout(self.main_widget)
        self.start_ban_pick_mode()

    # 선픽 팀 선택 함수 (일반 모드)
    def select_first_normal_team1(self):
        self.pick_order = self.default_pick_order
        self.current_pick = 0

        self.clear_layout(self.main_widget)
        self.start_normal_pick_mode()
    
    # 선픽 팀 선택 함수 (일반 모드)
    def select_first_normal_team2(self):
        self.pick_order = self.alternate_pick_order
        self.current_pick = 0

        self.clear_layout(self.main_widget)
        self.start_normal_pick_mode()
    
    def update_time(self):
        """시간 기록을 1초마다 업데이트"""
        self.time_counter += 1
        self.time_label.setText(str(self.time_counter))
        if(self.time_counter%60 == 0):
            pygame.mixer.music.load(self.siren_path)  # 사운드 파일 경로 설정
            pygame.mixer.music.play()  # 사운드 재생

    # 밴픽 모드 시작 함수
    def start_ban_pick_mode(self):
        self.is_ban_phase = True  # 밴 단계 시작 설정
        layout = self.main_widget.layout()  # 기존 레이아웃을 가져옵니다.
        
        # 캐릭터 버튼 영역 설정
        character_frame = QWidget()
        character_layout = QGridLayout()
        character_frame.setLayout(character_layout)

        for i, character in enumerate(self.characters):
            if character["name"] in self.eternel_ban_characters:
                continue

            img = character["image"].scaled(80, 80)

            button_container = QWidget()
            button_layout = QVBoxLayout(button_container)
            button_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
            button_layout.setSpacing(0)  # 버튼과 이름 라벨 간의 간격 제거

            
            button = QPushButton()
            button.setIcon(QIcon(img))
            button.setIconSize(QSize(80, 80))
            button.setFixedSize(80, 80)  # 버튼 크기를 이미지 크기와 맞춤
            button.setStyleSheet("border: none;")  # 버튼의 테두리 제거

            # 버튼 아래쪽에 이름을 표시하는 레이아웃 추가
            name_label = QLabel(character["name"])
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 6pt;")  # 폰트 크기 조정
            name_label.setFixedSize(80, 30)  # 라벨 크기 고정

            button_layout.addWidget(button, alignment=Qt.AlignTop)
            button_layout.addWidget(name_label, alignment=Qt.AlignBottom)
            
            button.clicked.connect(lambda _, c=character, b=button: (
                self.select_ban_character(c, b, "ban"),  # 로컬에서 캐릭터 선택 함수 호출
                self.chat_app.send_btn(f"select_ban_character:{c['name']}")  # 상대방에 캐릭터 선택 신호 전송
            ))
            character_layout.addWidget(button_container, i // 20, i % 20)
            self.character_buttons[character["name"]] = button

        # 밴 캐릭터 표시 영역
        ban_frame = QFrame()
        ban_layout = QHBoxLayout()
        ban_frame.setLayout(ban_layout)
        ban_frame.setStyleSheet("border: 1px solid black; padding: 5px;")  # 네모 테두리 추가

        self.team1_ban_frame = QFrame()
        self.team2_ban_frame = QFrame()
        self.team1_ban_frame.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.team2_ban_frame.setStyleSheet("border: 1px solid black; padding: 5px;")
        team1_layout = QGridLayout()
        team2_layout = QGridLayout()
        self.team1_ban_frame.setLayout(team1_layout)
        self.team2_ban_frame.setLayout(team2_layout)

        for i in range(5):
            label1 = QLabel(f"밴 {i+1}")
            label1.setFixedWidth(90)  # 라벨 가로 크기를 90으로 설정
            label1.setFixedHeight(90)
            team1_layout.addWidget(label1, 0, i)
            label2 = QLabel(f"밴 {i+1}")
            label2.setFixedWidth(90)  # 라벨 가로 크기를 90으로 설정
            label2.setFixedHeight(90)
            team2_layout.addWidget(label2, 0, i)
        

        # 픽 상태 표시 라벨
        self.current_status_label = QLabel("")
        self.current_status_label.setAlignment(Qt.AlignCenter)  # 가로 중앙 정렬
        self.current_status_label.setStyleSheet("font-size: 50px;")

        ban_layout.setContentsMargins(0, 0, 0, 0)
        ban_layout.addWidget(self.team1_ban_frame)
        ban_layout.addWidget(self.current_status_label)
        ban_layout.addWidget(self.team2_ban_frame)
        
        # 선택된 캐릭터 표시 영역
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)

        # 네모 테두리 스타일 적용
        bottom_frame.setStyleSheet("border: 1px solid black;")

        self.team1_frame = QFrame()
        self.team2_frame = QFrame()
        team1_layout = QGridLayout()
        team2_layout = QGridLayout()
        self.team1_frame.setLayout(team1_layout)
        self.team2_frame.setLayout(team2_layout)

        for i in range(3):
            slot_label1 = QLabel(f"Slot {i+1}")
            slot_label1.setFixedWidth(90)  # 가로 크기를 90으로 설정
            slot_label1.setFixedHeight(90)
            team1_layout.addWidget(slot_label1, 0, i)

            slot_label2 = QLabel(f"Slot {i+1}")
            slot_label2.setFixedWidth(90)  # 가로 크기를 90으로 설정
            slot_label2.setFixedHeight(90)
            team2_layout.addWidget(slot_label2, 0, i)

        # 시간 기록용 레이블 초기화
        self.time_label = QLabel("0")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 16pt; font-family: Arial;")

        # 1초마다 시간 기록을 업데이트하는 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1초마다 업데이트

        # 초기 시간 설정
        self.time_counter = 0

        bottom_layout.addWidget(self.team1_frame)
        bottom_layout.addWidget(self.time_label)
        bottom_layout.addWidget(self.team2_frame)

        # 레이아웃 설정
        layout.addWidget(character_frame)
        layout.addWidget(ban_frame)
        layout.addWidget(bottom_frame)
        self.update_next_status()

    def start_normal_pick_mode(self):
        layout = self.main_widget.layout()  # 기존 레이아웃을 가져옵니다.

        # 캐릭터 버튼 영역
        character_frame = QWidget()
        character_layout = QGridLayout()
        character_frame.setLayout(character_layout)

        for i, character in enumerate(self.characters):
            if character["name"] in self.eternel_ban_characters:
                continue
            
            img = character["image"].scaled(80, 80)

            button_container = QWidget()
            button_layout = QVBoxLayout(button_container)
            button_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
            button_layout.setSpacing(0)  # 버튼과 이름 라벨 간의 간격 제거

            
            button = QPushButton()
            button.setIcon(QIcon(img))
            button.setIconSize(QSize(80, 80))
            button.setFixedSize(80, 80)  # 버튼 크기를 이미지 크기와 맞춤
            button.setStyleSheet("border: none;")  # 버튼의 테두리 제거

            # 버튼 아래쪽에 이름을 표시하는 레이아웃 추가
            name_label = QLabel(character["name"])
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 6pt;")  # 폰트 크기 조정
            name_label.setFixedSize(80, 30)  # 라벨 크기 고정

            button_layout.addWidget(button, alignment=Qt.AlignTop)
            button_layout.addWidget(name_label, alignment=Qt.AlignBottom)
            
            button.clicked.connect(lambda _, c=character, b=button: (
                self.select_character(c, b),  # 로컬에서 캐릭터 선택 함수 호출
                self.chat_app.send_btn(f"select_character:{c['name']}")  # 상대방에 캐릭터 선택 신호 전송
            ))
            character_layout.addWidget(button_container, i // 20, i % 20)
            self.character_buttons[character["name"]] = button

        # 픽 상태 표시 라벨
        self.current_status_label = QLabel("")
        self.current_status_label.setStyleSheet("font-size: 50px;")

        # 선택된 캐릭터 표시 영역
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)

        # 네모 테두리 스타일 적용
        bottom_frame.setStyleSheet("border: 1px solid black;")

        self.team1_frame = QFrame()
        self.team2_frame = QFrame()
        team1_layout = QGridLayout()
        team2_layout = QGridLayout()
        self.team1_frame.setLayout(team1_layout)
        self.team2_frame.setLayout(team2_layout)

        for i in range(3):
            slot_label1 = QLabel(f"Slot {i+1}")
            slot_label1.setFixedWidth(90)  # 가로 크기를 90으로 설정
            slot_label1.setFixedHeight(90)
            team1_layout.addWidget(slot_label1, 0, i)

            slot_label2 = QLabel(f"Slot {i+1}")
            slot_label2.setFixedWidth(90)  # 가로 크기를 90으로 설정
            slot_label2.setFixedHeight(90)
            team2_layout.addWidget(slot_label2, 0, i)

        # 시간 기록용 레이블 초기화
        self.time_label = QLabel("0")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 16pt; font-family: Arial;")

        # 1초마다 시간 기록을 업데이트하는 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1초마다 업데이트

        # 초기 시간 설정
        self.time_counter = 0

        bottom_layout.addWidget(self.team1_frame)
        bottom_layout.addWidget(self.current_status_label)
        bottom_layout.addWidget(self.time_label)
        bottom_layout.addWidget(self.team2_frame)

        # 기존 레이아웃에 위젯 추가
        layout.addWidget(character_frame)
        layout.addWidget(bottom_frame)
        self.update_next_status()
    
    def update_next_status(self):
        # 밴픽 모드일 경우
        if self.is_ban_phase and self.current_ban < 6:
            team, team_name = self.ban_order[self.current_ban]
            self.current_status_label.setText(f"{team_name} 밴")
        elif self.is_ban_phase2 and self.current_ban < 10:
            team, team_name = self.ban_order[self.current_ban]
            self.current_status_label.setText(f"{team_name} 밴")
        # 일반 모드 또는 픽 단계일 경우
        elif self.current_pick < len(self.pick_order):
            team, team_name = self.pick_order[self.current_pick]
            self.current_status_label.setText(f"{team_name} 픽")

    def select_ban_character(self, character, button, phase):
        # 밴 단계 처리
        if phase == "ban":
            if self.current_ban < 6:
                team, team_name = self.ban_order[self.current_ban]
                self.bans[team_name].append(character)
                self.update_ban_display(team_name)
                button.hide()  # 버튼을 숨깁니다
                self.current_ban += 1
                self.time_counter = 0
                self.time_label.setText(str(self.time_counter))
                # 버튼 클릭 시 사운드 재생
                pygame.mixer.music.load(self.sound_path)  # 사운드 파일 경로 설정
                pygame.mixer.music.play()  # 사운드 재생

                # 밴이 완료되면 픽 단계로 전환
                if self.current_ban >= 6:
                    self.is_ban_phase = False
                    QMessageBox.information(self, "Info", "1차 밴 완료! 이제 1차 픽을 시작합니다.")
                self.update_next_status()
            elif self.current_ban < 10 and self.current_pick >= 4:
                # 밴이 완료되었으면 픽 단계로 넘김
                self.select_ban_character(character, button, "ban2")
            else:
                # 밴이 완료되었으면 픽 단계로 넘김
                self.select_ban_character(character, button, "pick")
        elif phase == "ban2":
            if self.current_ban < 10:
                team, team_name = self.ban_order[self.current_ban]
                self.bans[team_name].append(character)
                self.update_ban_display(team_name)
                button.hide()  # 버튼을 숨깁니다
                self.current_ban += 1
                self.time_counter = 0
                self.time_label.setText(str(self.time_counter))
                # 버튼 클릭 시 사운드 재생
                pygame.mixer.music.load(self.sound_path)  # 사운드 파일 경로 설정
                pygame.mixer.music.play()  # 사운드 재생

                # 밴이 완료되면 픽 단계로 전환
                if self.current_ban >= 10:
                    self.is_ban_phase2 = False
                    QMessageBox.information(self, "Info", "2차 밴 완료! 이제 2차 픽을 시작합니다.")
                self.update_next_status()
            else:
                # 밴이 완료되었으면 픽 단계로 넘김
                self.select_ban_character(character, button, "pick2")
        # 픽 단계 처리
        elif phase == "pick":
            if self.current_pick < len(self.pick_order):
                team, team_name = self.pick_order[self.current_pick]
                self.picks[team_name].append(character)
                self.update_picks_display(team_name)
                button.hide()  # 버튼을 숨깁니다
                self.current_pick += 1
                self.time_counter = 0
                self.time_label.setText(str(self.time_counter))
                # 버튼 클릭 시 사운드 재생
                pygame.mixer.music.load(self.sound_path)  # 사운드 파일 경로 설정
                pygame.mixer.music.play()  # 사운드 재생

                if self.current_pick == 4 and self.current_ban == 6 :
                    self.is_ban_phase2 = True
                    QMessageBox.information(self, "Info", "1차 픽 완료! 이제 2차 밴을 시작합니다.")
                    self.update_next_status()
                # 모든 픽이 완료되었을 경우 최종 화면 표시
                elif self.current_pick >= len(self.pick_order):
                    self.show_final_ban_selection()
                    self.current_status_label.setText("")  # 상태 초기화
                else:
                    self.update_next_status()
            # 픽 단계 처리
        elif phase == "pick2":
            if self.current_pick < len(self.pick_order):
                team, team_name = self.pick_order[self.current_pick]
                self.picks[team_name].append(character)
                self.update_picks_display(team_name)
                button.hide()  # 버튼을 숨깁니다
                self.current_pick += 1
                self.time_counter = 0
                self.time_label.setText(str(self.time_counter))
                # 버튼 클릭 시 사운드 재생
                pygame.mixer.music.load(self.sound_path)  # 사운드 파일 경로 설정
                pygame.mixer.music.play()  # 사운드 재생

                # 모든 픽이 완료되었을 경우 최종 화면 표시
                if self.current_pick >= len(self.pick_order):
                    self.show_final_ban_selection()
                    self.current_status_label.setText("")  # 상태 초기화
                else:
                    self.update_next_status()
    
    # 밴 캐릭터 표시 함수
    def update_ban_display(self, team_name):
        team_frame = self.team1_ban_frame if team_name == "Team 1" else self.team2_ban_frame
        layout = team_frame.layout()
        
        # 팀의 밴 리스트에 있는 캐릭터를 표시
        for i, ban in enumerate(self.bans[team_name]):
            img = ban["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: lightgray;")
            layout.addWidget(img_label, 0, i)

    # 선택된 캐릭터 업데이트 함수
    def update_picks_display(self, team_name):
        team_frame = self.team1_frame if team_name == "Team 1" else self.team2_frame
        layout = team_frame.layout()
        
        # 팀의 픽 리스트에 있는 캐릭터를 표시
        for i, pick in enumerate(self.picks[team_name]):
            img = pick["image"].scaled(80, 80)
            
            # 이미지 라벨
            img_label = QLabel()
            img_label.setPixmap(img)
            layout.addWidget(img_label, 0, i)
            
            # 이름 라벨
            name_label = QLabel(pick["name"])
            name_label.setStyleSheet("font-size: 10pt; font-family: Arial;")
            layout.addWidget(name_label, 1, i)
    
    # 일반 모드의 캐릭터 선택 함수 (픽)
    def select_character(self, character, button):
        # 현재 픽이 모든 픽 순서를 초과했는지 확인
        if self.current_pick >= len(self.pick_order):
            QMessageBox.information(self, "Info", "픽 완료!")
            return
        
        # 현재 순서의 팀과 팀 이름을 가져와 캐릭터를 추가
        team, team_name = self.pick_order[self.current_pick]
        self.picks[team_name].append(character)
        button.hide()  # 버튼을 삭제하여 화면에서 제거
        self.update_picks_display(team_name)
        self.current_pick += 1
        self.time_counter = 0
        self.time_label.setText(str(self.time_counter))
        # 버튼 클릭 시 사운드 재생
        pygame.mixer.music.load(self.sound_path)  # 사운드 파일 경로 설정
        pygame.mixer.music.play()  # 사운드 재생

        # 모든 픽이 완료되었을 경우 최종 화면 표시
        if self.current_pick >= len(self.pick_order):
            self.show_final_selection()
            self.current_status_label.setText("")  # 모든 픽이 완료된 후 상태 초기화
        else:
            # 다음 순서 상태 표시
            self.update_next_status()

    # 최종 선택된 밴 및 픽 캐릭터 화면 표시 함수
    def show_final_ban_selection(self):
        self.timer.stop()
        # 기존 위젯을 모두 제거
        self.clear_layout(self.main_widget)
        layout = self.main_widget.layout()  # 기존 레이아웃을 가져옵니다.

        # 최종 캐릭터 선택 화면 구성
        self.final_frame = QFrame(self.main_widget)
        final_layout = QGridLayout(self.final_frame)
        self.final_frame.setLayout(final_layout)

        # 1팀 영역
        self.team1_final_frame = QFrame()
        team1_layout = QGridLayout(self.team1_final_frame)
        final_layout.addWidget(self.team1_final_frame, 0, 0, alignment=Qt.AlignRight)

        team1_label = QLabel("1팀")
        team1_label.setStyleSheet("font-size: 16pt; font-family: Arial;")
        team1_layout.addWidget(team1_label, 0, 0, 1, 5, alignment=Qt.AlignCenter)

        # 팀 1의 밴 캐릭터 표시
        for i, ban in enumerate(self.bans["Team 1"]):
            img = ban["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: lightgray;")
            team1_layout.addWidget(img_label, 1, i, alignment=Qt.AlignCenter)
            name_label = QLabel(ban["name"])
            name_label.setStyleSheet("font-size: 10pt;")
            team1_layout.addWidget(name_label, 2, i, alignment=Qt.AlignCenter)

        # 팀 1의 픽 캐릭터 표시
        for i, pick in enumerate(self.picks["Team 1"]):
            img = pick["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: green;")
            team1_layout.addWidget(img_label, 3, i, alignment=Qt.AlignCenter)
            name_label = QLabel(pick["name"])
            name_label.setStyleSheet("font-size: 10pt;")
            team1_layout.addWidget(name_label, 4, i, alignment=Qt.AlignCenter)

        # 2팀 영역
        self.team2_final_frame = QFrame()
        team2_layout = QGridLayout(self.team2_final_frame)
        final_layout.addWidget(self.team2_final_frame, 0, 2, alignment=Qt.AlignLeft)

        team2_label = QLabel("2팀")
        team2_label.setStyleSheet("font-size: 16pt; font-family: Arial;")
        team2_layout.addWidget(team2_label, 0, 0, 1, 5, alignment=Qt.AlignCenter)

        # 팀 2의 밴 캐릭터 표시
        for i, ban in enumerate(self.bans["Team 2"]):
            img = ban["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: lightgray;")
            team2_layout.addWidget(img_label, 1, i, alignment=Qt.AlignCenter)
            name_label = QLabel(ban["name"])
            name_label.setStyleSheet("font-size: 10pt;")
            team2_layout.addWidget(name_label, 2, i, alignment=Qt.AlignCenter)

        # 팀 2의 픽 캐릭터 표시
        for i, pick in enumerate(self.picks["Team 2"]):
            img = pick["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: green;")
            team2_layout.addWidget(img_label, 3, i, alignment=Qt.AlignCenter)
            name_label = QLabel(pick["name"])
            name_label.setStyleSheet("font-size: 10pt;")
            team2_layout.addWidget(name_label, 4, i, alignment=Qt.AlignCenter)

        # 승리 버튼들 표시
        self.win_button_frame = QFrame()
        win_button_layout = QHBoxLayout(self.win_button_frame)
        final_layout.addWidget(self.win_button_frame, 1, 1, alignment=Qt.AlignCenter)

        team1_win_button = QPushButton("1팀 승리")
        team1_win_button.setFixedSize(150, 50)
        team1_win_button.clicked.connect(lambda: (self.declare_winner1(), self.chat_app.send_btn("declare_winner1")))
        win_button_layout.addWidget(team1_win_button)

        team2_win_button = QPushButton("2팀 승리")
        team2_win_button.setFixedSize(150, 50)
        team2_win_button.clicked.connect(lambda: (self.declare_winner2(), self.chat_app.send_btn("declare_winner2")))
        win_button_layout.addWidget(team2_win_button)

        layout.addWidget(self.final_frame)
    

    # 최종 선택된 캐릭터 화면 표시 함수
    def show_final_selection(self):
        self.timer.stop()
        # 기존 위젯을 모두 제거
        self.clear_layout(self.main_widget)
        layout = self.main_widget.layout()  # 기존 레이아웃을 가져옵니다.

        # 최종 캐릭터 선택 화면 구성
        self.final_frame = QFrame(self.main_widget)
        final_layout = QGridLayout(self.final_frame)
        self.final_frame.setLayout(final_layout)

        # 1팀 영역
        self.team1_final_frame = QFrame()
        team1_layout = QGridLayout(self.team1_final_frame)
        final_layout.addWidget(self.team1_final_frame, 0, 0, alignment=Qt.AlignRight)

        team1_label = QLabel("1팀")
        team1_label.setStyleSheet("font-size: 16pt; font-family: Arial;")
        team1_layout.addWidget(team1_label, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        # 팀 1의 픽 캐릭터 표시
        for i, pick in enumerate(self.picks["Team 1"]):
            img = pick["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: green;")
            team1_layout.addWidget(img_label, 1, i, alignment=Qt.AlignCenter)
            name_label = QLabel(pick["name"])
            name_label.setStyleSheet("font-size: 10pt;")
            team1_layout.addWidget(name_label, 2, i, alignment=Qt.AlignCenter)

        # 2팀 영역
        self.team2_final_frame = QFrame()
        team2_layout = QGridLayout(self.team2_final_frame)
        final_layout.addWidget(self.team2_final_frame, 0, 2, alignment=Qt.AlignLeft)

        team2_label = QLabel("2팀")
        team2_label.setStyleSheet("font-size: 16pt; font-family: Arial;")
        team2_layout.addWidget(team2_label, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        # 팀 2의 픽 캐릭터 표시
        for i, pick in enumerate(self.picks["Team 2"]):
            img = pick["image"].scaled(80, 80)
            img_label = QLabel()
            img_label.setPixmap(img)
            img_label.setStyleSheet("background-color: green;")
            team2_layout.addWidget(img_label, 1, i, alignment=Qt.AlignCenter)
            name_label = QLabel(pick["name"])
            name_label.setStyleSheet("font-size: 10pt;")
            team2_layout.addWidget(name_label, 2, i, alignment=Qt.AlignCenter)

        # 승리 버튼들 표시
        self.win_button_frame = QFrame()
        win_button_layout = QHBoxLayout(self.win_button_frame)
        final_layout.addWidget(self.win_button_frame, 1, 1, alignment=Qt.AlignCenter)

        team1_win_button = QPushButton("1팀 승리")
        team1_win_button.setFixedSize(150, 50)
        team1_win_button.clicked.connect(lambda: (self.declare_winner1(), self.chat_app.send_btn("declare_winner1")))
        win_button_layout.addWidget(team1_win_button)

        team2_win_button = QPushButton("2팀 승리")
        team2_win_button.setFixedSize(150, 50)
        team2_win_button.clicked.connect(lambda: (self.declare_winner2(), self.chat_app.send_btn("declare_winner2")))
        win_button_layout.addWidget(team2_win_button)

        layout.addWidget(self.final_frame)

    # 승리 팀의 레이아웃 스타일을 변경하는 함수
    def style_winning_team(self, frame):
        # 내부의 모든 위젯에 대해 배경색과 글자색을 변경
        for i in range(frame.layout().count()):
            widget = frame.layout().itemAt(i).widget()
            if widget is not None:
                widget.setStyleSheet("background-color: green; color: white;")
                if isinstance(widget, QLabel):
                    widget.setStyleSheet("color: white;")

    # 승리 버튼 클릭 시 처리 함수
    def declare_winner1(self):
        self.team1_final_frame.setStyleSheet("background-color: green;")
        self.style_winning_team(self.team1_final_frame)
        # 승리 버튼 숨기기
        self.win_button_frame.hide()
    
    # 승리 버튼 클릭 시 처리 함수
    def declare_winner2(self):
        self.team2_final_frame.setStyleSheet("background-color: green;")
        self.style_winning_team(self.team2_final_frame)
        # 승리 버튼 숨기기
        self.win_button_frame.hide()
