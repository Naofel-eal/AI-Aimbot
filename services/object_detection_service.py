from torch import set_flush_denormal, cuda
from super_gradients.common.object_names import Models
from super_gradients.training import models
from utils.logger import Logger

class ObjectDetectionService:
    
    def __init__(self, checkpoint_path='./checkpoints/ckpt_best.pth', logger=None) -> None:
        self.logger = Logger() if logger is None else logger
        self.checkpoint_path = checkpoint_path
        self.device = 'cuda' if cuda.is_available() else "cpu"
        self.model = self.load_model()
        self.logger.info(f"Successfully loaded model.")
        self.logger.info(f"Selected device: {self.device.upper()}.")
        self.logger.info(f"Object detection service initialized.")
        
    def load_model(self):
        """
        Load the YOLO model and return it.
        """
        set_flush_denormal(True)
        self.logger.info(f"Loading model...")
        model = models.get(Models.YOLO_NAS_S, checkpoint_path=self.checkpoint_path, num_classes=2)
        model = model.to(self.device)
        return model
    
    def process_frame(self, frame):
        """
        Run object detection using the provided model.
        """
        result = self.model.predict(frame)
        return result

    def get_prediction_info(self, predictions):
        """
        Get the bounding boxes, confidence, labels and class names from the prediction.
        """
        results = []
        for image_prediction in predictions:
            class_names = image_prediction.class_names
            labels = image_prediction.prediction.labels
            confidence = image_prediction.prediction.confidence
            bboxes = image_prediction.prediction.bboxes_xyxy
            results.append((bboxes, confidence, labels, class_names))
        return results

       
