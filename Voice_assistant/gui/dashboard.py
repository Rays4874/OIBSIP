from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QLabel, QPushButton, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

class VectorDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vector AI - Project Sentinel")
        self.setGeometry(100, 100, 1000, 600)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #0f111a; }
            QLabel { color: #82aaff; font-family: 'Consolas'; }
            QTextEdit { 
                background-color: #1a1c23; 
                color: #c3e88d; 
                border: 1px solid #82aaff; 
                font-family: 'Consolas';
                font-size: 14px;
                padding: 10px;
            }
            QPushButton {
                background-color: #82aaff;
                color: #0f111a;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #a6c8ff; }
            QFrame { border: 1px solid #3b4252; border-radius: 5px; background-color: #1a1c23; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)


        left_panel = QVBoxLayout()
        
        self.status_frame = QFrame()
        status_layout = QVBoxLayout(self.status_frame)
        self.status_title = QLabel("🖥️ SYSTEM STATUS")
        self.status_title.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        self.cpu_label = QLabel("CPU: --%")
        self.ram_label = QLabel("RAM: --%")
        self.bat_label = QLabel("BAT: --%")
        status_layout.addWidget(self.status_title)
        status_layout.addWidget(self.cpu_label)
        status_layout.addWidget(self.ram_label)
        status_layout.addWidget(self.bat_label)
        
        self.memory_frame = QFrame()
        memory_layout = QVBoxLayout(self.memory_frame)
        self.memory_title = QLabel("🧠 ACTIVE PROFILE")
        self.memory_title.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        self.memory_details = QLabel("Loading...")
        self.memory_details.setWordWrap(True)
        memory_layout.addWidget(self.memory_title)
        memory_layout.addWidget(self.memory_details)

        left_panel.addWidget(self.status_frame)
        left_panel.addWidget(self.memory_frame)
        left_panel.addStretch()


        right_panel = QVBoxLayout()
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        
        bottom_bar = QHBoxLayout()
        self.indicator = QLabel("🔴 OFFLINE")
        self.indicator.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        
        self.start_btn = QPushButton("INITIALIZE VECTOR")
        self.start_btn.clicked.connect(self.start_ai)
        
        bottom_bar.addWidget(self.indicator)
        bottom_bar.addWidget(self.start_btn)
        
        right_panel.addWidget(self.chat_display)
        right_panel.addLayout(bottom_bar)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 3)

        self.ai_thread = None

    def start_ai(self):
        if self.ai_thread is None:
            from main import AIEngineThread # Imported here to avoid circular imports
            
            self.ai_thread = AIEngineThread()
            self.ai_thread.log_signal.connect(self.update_chat)
            self.ai_thread.state_signal.connect(self.update_indicator)
            self.ai_thread.stats_signal.connect(self.update_system_stats)
            self.ai_thread.profile_signal.connect(self.update_profile)
            
            self.ai_thread.start()
            self.start_btn.setText("SYSTEM ONLINE")
            self.start_btn.setEnabled(False)

    def update_chat(self, text):
        self.chat_display.append(text)
        
    def update_indicator(self, state):
        if state == "listening":
            self.indicator.setText("🟡 LISTENING...")
            self.indicator.setStyleSheet("color: #ffcb6b;")
        elif state == "processing":
            self.indicator.setText("🟢 PROCESSING...")
            self.indicator.setStyleSheet("color: #c3e88d;")
        elif state == "speaking":
            self.indicator.setText("🔵 SPEAKING...")
            self.indicator.setStyleSheet("color: #82aaff;")
        elif state == "standby": 
            self.indicator.setText("💤 STANDBY...") 
            self.indicator.setStyleSheet("color: #676E95;") 
            
    def update_system_stats(self, cpu, ram, bat):
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram}%")
        self.bat_label.setText(f"BAT: {bat}")
        
    def update_profile(self, profile_text):
        self.memory_details.setText(profile_text)