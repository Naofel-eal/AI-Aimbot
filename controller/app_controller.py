from time import sleep, perf_counter
from win32.win32api import GetAsyncKeyState
from win32con import VK_F1, VK_F2, VK_F12
from PyQt5.QtCore import QThread, pyqtSignal

class AppController(QThread):
    f12_pressed = pyqtSignal()
    new_cheat_state = pyqtSignal(bool)
    new_rendering_mode_state = pyqtSignal(bool)
    send_fps = pyqtSignal(float)

    def __init__(self, logger, object_detection_service, capture_service, frame_renderer_service, configuration):
        super().__init__()
        self.load_data_from_config(configuration)
        self.logger = logger
        self.object_detection_service = object_detection_service
        self.capture_service = capture_service
        self.frame_renderer_service = frame_renderer_service
        self.is_cheat_enabled = True
        self.is_rendering_mode_enabled = False        

    def load_data_from_config(self, configuration):       
        self.DELAY_ON_KEY_PRESS = configuration['DELAY_ON_KEY_PRESS']
        self.DELAY_BEFORE_UPDATE_FPS = configuration['DELAY_BEFORE_UPDATE_FPS']
        
    def init_signals(self, overlay):
        self.new_cheat_state.connect(overlay.set_cheat_state)
        self.new_rendering_mode_state.connect(overlay.set_rendering_mode_state)
        self.send_fps.connect(overlay.set_fps)

    def check_key_toggle(self, key_code, on_toggle, description):
        if GetAsyncKeyState(key_code) != 0:
            state = on_toggle()
            self.logger.info(f"{description} status: {'enabled' if state else 'disabled'}")
            self.new_rendering_mode_state.emit(self.is_rendering_mode_enabled)
            self.new_cheat_state.emit(self.is_cheat_enabled)
            sleep(self.DELAY_ON_KEY_PRESS)

    def on_cheat_toggle(self):
        self.is_cheat_enabled = not self.is_cheat_enabled
        if self.is_cheat_enabled:
            self.capture_service.start_performance_counter()
        else:
            self.is_rendering_mode_enabled = False
            self.frame_renderer_service.stop()
            fps = 0
            self.send_fps.emit(fps)
            
        return self.is_cheat_enabled

    def on_rendering_mode_toggle(self):
        self.is_rendering_mode_enabled = not self.is_rendering_mode_enabled
        if not self.is_rendering_mode_enabled:
            self.frame_renderer_service.stop()
        self.capture_service.start_performance_counter()
        
        return self.is_rendering_mode_enabled

    def run(self):
        self.logger.manual()
        
        fps = 0
        last_fps_update = perf_counter()
        self.capture_service.start_performance_counter()

        while GetAsyncKeyState(VK_F12) == 0:
            self.check_key_toggle(VK_F1, self.on_cheat_toggle, "Cheat")
            self.check_key_toggle(VK_F2, self.on_rendering_mode_toggle, "Rendering mode")

            if self.is_cheat_enabled:
                frame = self.capture_service.capture()
                if frame is not None:
                    prediction = self.object_detection_service.process_frame(frame)
                    if self.is_rendering_mode_enabled:
                        self.frame_renderer_service.render(frame, fps)
                fps = self.capture_service.get_fps()
                
                current_time = perf_counter()
                elapsed_time = current_time - last_fps_update
                if elapsed_time >= self.DELAY_BEFORE_UPDATE_FPS:
                    self.send_fps.emit(fps)
                    last_fps_update = current_time

        self.logger.fps(fps)
        self.frame_renderer_service.stop()
        self.f12_pressed.emit()
        self.logger.info("Exiting...")