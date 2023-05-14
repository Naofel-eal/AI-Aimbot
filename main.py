from sys import exit, argv
from PyQt5.QtWidgets import QApplication

from models.overlay import Overlay
from configurations.config_loader import ConfigLoader
from services.capture_service import CaptureService
from services.object_detection_service import ObjectDetectionService
from services.frame_renderer_service import FrameRendererService
from utils.logger import Logger
from controllers.app_controller import AppController

def main():
    # Initialize services
    logger = Logger()
    configuration = ConfigLoader(logger).load()
    object_detection_service = ObjectDetectionService(logger=logger)
    capture_service = CaptureService(configuration['capture'], logger=logger)
    frame_renderer_service = FrameRendererService(display_fps=False, logger=logger)

    # Create the AppController
    app_controller = AppController(logger, object_detection_service, capture_service, frame_renderer_service, configuration['main'])

    # Create and show the overlay
    app = QApplication(argv)
    app_controller.f12_pressed.connect(app.quit)
    overlay = Overlay(configuration['gui'])
    app_controller.init_signals(overlay)
    overlay.show()

    # Start the app_controller
    app_controller.start()
    app.exec_()
    exit(0)

if __name__ == '__main__':
    main()