import dxshot
from time import perf_counter
from cv2 import imshow, waitKey
from utils.logger import Logger

class CaptureService:
    
    def __init__(self, configuration, output_idx=0, output_color="BGR", window_name="Capture", logger=None) -> None:
        self.logger = Logger() if logger is None else logger
        self.frame_counter = 0
        self.fps_average = 0
        self.FPS_COMPUTATION_FRAME_COUNT = configuration['FPS_COMPUTATION_FRAME_COUNT']
        self.window_name = window_name
        self.cam = dxshot.create(output_idx=output_idx, output_color=output_color)
        self.logger.info("Capture service initialized.")
        
    def start_performance_counter(self):
        """
        Start the camera and performance counter.
        """
        self.fps = 0
        self.frame_counter = 0
        self.start_time = perf_counter()
                
    def capture(self):
        """
        Get the latest frame from the camera buffer.
        Returns:
            A frame from the camera buffer.
        """
        
        if self.frame_counter == self.FPS_COMPUTATION_FRAME_COUNT:
            self.start_performance_counter()
        self.frame_counter += 1
        return self.cam.grab()

    def get_fps(self):
        """
        Compute the FPS of the capture (does not display it).
        Returns:
            The average FPS.
        """
        self.fps_average = self.frame_counter / (perf_counter() - self.start_time)
        return round(self.fps_average, 2)
            
    def test_max_performance(self, render=False, frame_limit=1000):
        """
        Test the maximum capture frames per second of the camera.
        Args:
            render: Whether to display the frames.
            frame_limit: Maximum number of frames to capture.
        Returns:
            The maximum FPS achieved.
        """
        self.logger.info("Starting capture performance test...")
        frame_counter = 0
        max_fps = 0
        fps_sum = 0
        start_time = perf_counter()
        
        while frame_counter < frame_limit:
            frame = self.cam.grab()
            if frame is not None:
                if render:
                    with imshow(self.window_name, frame):
                        waitKey(1)
                frame_counter += 1
                fps = frame_counter / (perf_counter() - start_time)
                fps_sum += fps
                #self.logger.fps(fps)
                max_fps = max(max_fps, fps)

        self.logger.info(f"Max FPS: {max_fps}")
        self.logger.info(f"Average FPS: {fps_sum / frame_counter}")
        return max_fps
