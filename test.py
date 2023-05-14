from services.capture_service import CaptureService
from services.object_detection_service import ObjectDetectionService
from services.frame_renderer_service import FrameRendererService
from utils.logger import Logger
from configurations.config_loader import ConfigLoader
import cv2
import time

def run_pt_inferences(object_detection_service, capture_service, inference_count=1):
    for i in range(5):
        frame = capture_service.capture()
        start_time = time.perf_counter_ns()
        prediction = object_detection_service.process_frame(frame)._images_prediction_lst[0]
        end_time = time.perf_counter_ns()
        print("Time: ", (end_time - start_time) / 1000000000)
        return prediction

def init():
    # Initialize services
    logger = Logger()
    configuration = ConfigLoader(logger).load()
    object_detection_service = ObjectDetectionService(logger=logger)
    capture_service = CaptureService(configuration['capture'], logger=logger)
    frame_renderer_service = FrameRendererService(display_fps=False, logger=logger)

    return object_detection_service, capture_service, frame_renderer_service
        
    
    confidence = prediction.prediction.confidence
    labels = prediction.prediction.labels
    class_names = prediction.class_names
    bboxes = prediction.prediction.bboxes_xyxy
    
    prediction.draw()
    image = prediction.image
    print(prediction)
    
    #print(labels)
    #print(class_names)
    #print(confidence)
    
    print(bboxes)
    cv2.imshow("test", image)
    cv2.waitKey(0)

if __name__ == '__main__':
    object_detection_service, capture_service, frame_renderer_service = init()
    prediction = run_pt_inferences(object_detection_service, capture_service, inference_count=1)
    image = prediction.image
    bboxes = prediction.prediction.bboxes_xyxy
    confidence = prediction.prediction.confidence
    labels = prediction.prediction.labels
    class_names = prediction.class_names
    
    detection = prediction.draw()
    cv2.imshow("test", detection)
    cv2.waitKey(0)
    
    