from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

class Overlay(QWidget):
    
    def __init__(self, configuration):
        super().__init__()
        self.load_data_from_config(configuration)
        self.init_attributes()
        self.init_ui()
        self.init_timer()
    
    def load_data_from_config(self, config):
        self.title = config['title']
        self.padding = int(config['padding'])
        self.background_color = QColor(*map(int, config['background_color'].split(',')))
        
        self.title_color = config['title_color']
        self.title_font_size = config['title_font_size']
        self.title_font_weight = config['title_font_weight']
        
        self.fps_label_color = config['fps_label_color']
        self.fps_label_font_size = config['fps_label_font_size']
        self.fps_label_font_weight = config['fps_label_font_weight']
        
        self.default_label_color = config['default_label_color']
        self.default_label_font_size = config['default_label_font_size']
        self.default_label_weight = config['default_label_font_weight']
        
        self.overlay_position = tuple(map(int, config['overlay_position'].split(',')))
        self.overlay_size = tuple(map(int, config['overlay_size'].split(',')))
        self.refresh_rate = int(config['refresh_rate'])

    def init_attributes(self):
        self.cheat_state = True
        self.rendering_mode_state = False
        self.fps = 0.00

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(self.refresh_rate) 

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)
        self.setGeometry(self.overlay_position[0], self.overlay_position[1], self.overlay_size[0], self.overlay_size[1])
                        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)

        self.title_label = QLabel(self.title, self)
        self.title_label.setStyleSheet(f'color: {self.title_color}; font-weight: {self.title_font_weight}; font-size: {self.title_font_size};')
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        spacer = QSpacerItem(20, self.padding, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.fps_label = QLabel(f'FPS: {self.fps}', self)
        self.fps_label.setAlignment(Qt.AlignCenter)
        self.fps_label.setStyleSheet(f'color: {self.fps_label_color}; font-size: {self.fps_label_font_size};')
        layout.addWidget(self.fps_label)

        self.cheat_status_label = QLabel(f'Cheat: {self.cheat_state}', self)
        layout.addWidget(self.cheat_status_label)

        self.rendering_mode_label = QLabel(f'Rendering mode: {self.rendering_mode_state}', self)
        layout.addWidget(self.rendering_mode_label)

        self.refresh()
        self.adjustSize()
        self.show()

    def set_fps(self, fps):
        self.fps = fps  # Update the FPS value, you can replace this with the actual FPS value
        self.fps_label.setText(f'FPS: {self.fps}')
        
    def set_cheat_state(self, state):
        self.cheat_state = state
        
    def set_rendering_mode_state(self, state):
        self.rendering_mode_state = state
        
    def refresh(self):
        states = {
            True: {'label': 'ON', 'color': 'green'},
            False: {'label': 'OFF', 'color': 'red'}
        }

        self.cheat_status_label.setText(f'Cheat status: {states[self.cheat_state]["label"]}')
        self.cheat_status_label.setStyleSheet(f'color: {states[self.cheat_state]["color"]}; font-size: {self.default_label_font_size}; font-weight: {self.default_label_weight};')
        
        self.rendering_mode_label.setText(f'Rendering mode status: {states[self.rendering_mode_state]["label"]}')
        self.rendering_mode_label.setStyleSheet(f'color: {states[self.rendering_mode_state]["color"]}; font-size: {self.default_label_font_size}; font-weight: {self.default_label_weight};')

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(self.background_color) # set background color
        painter.setPen(QPen(QColor(255, 255, 255, 255), 2)) # set border color
        painter.drawRect(self.rect())