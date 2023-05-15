from torch import set_flush_denormal, cuda
from super_gradients.common.object_names import Models
from super_gradients.training import models
from utils.logger import Logger
from ultralytics import YOLO

class ObjectDetectionService:
    
    def __init__(self, model_type='yolo_nas_s', logger=None) -> None:
        self.logger = Logger() if logger is None else logger
        self.model_type = model_type if model_type == 'yolo_nas_s' else 'yolov8'
        self.checkpoint_path= './checkpoints/yolo_nas_s.pth' if model_type == 'yolo_nas_s' else './checkpoints/yolov8.pt'
        self.device = 'cuda' if cuda.is_available() else "cpu"
        self.model = self.load_model()
        self.logger.info(f"Successfully loaded model.")
        self.logger.info(f"Selected device: {self.device.upper()}.")
        self.logger.info(f"Object detection service initialized.")
        
    def load_model(self):
        """
        Load the YOLO model and return it.
        """
        if self.model_type == 'yolo_nas_s':
            set_flush_denormal(True)
            self.logger.info(f"Loading model...")
            model = models.get(Models.YOLO_NAS_S, checkpoint_path=self.checkpoint_path, num_classes=2)
            model = model.to(self.device)
        
        else:
            model = YOLO(self.checkpoint_path) 
        
        return model
    
    def process_frame(self, frame):
        """
        Run object detection using the provided model.
        """
        if self.model_type == 'yolo_nas_s':
            result = self.model.predict(frame)._images_prediction_lst[0].draw()
        else:
            result = self.model(frame)
        return result

    def get_prediction_info(self, prediction):
        """
        Get the bounding boxes, confidence, labels and class names from the prediction.
        """
        original_simage = prediction.image
        bboxes = prediction.prediction.bboxes_xyxy
        confidence = prediction.prediction.confidence
        labels = prediction.prediction.labels
        class_names = prediction.class_names

       
