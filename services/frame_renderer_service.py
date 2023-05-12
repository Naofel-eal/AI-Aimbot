from cv2 import putText, imshow, waitKey, FONT_HERSHEY_SIMPLEX, destroyAllWindows
from utils.logger import Logger

class FrameRendererService:
    def __init__(self, display_fps=False, logger=None) -> None:
        self.logger = Logger() if logger is None else logger
        self.display_fps = display_fps
        self.logger.info("Frame renderer initialized.")

    def render(self, frame, fps=0):
        if self.display_fps:
            fps_text = f"FPS: {fps}" 
            putText(frame, fps_text, (10, 30), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        imshow("Render", frame)
        waitKey(1)

    def stop(self):
        destroyAllWindows()
