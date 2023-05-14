from super_gradients.common.object_names import Models
from super_gradients.training import models
import torch

model = models.get(Models.YOLO_NAS_S, checkpoint_path='checkpoints/model.pth', num_classes=2)

model.eval()
model.prep_model_for_conversion(input_size=[1, 3, 640, 640])
    
dummy_input = torch.randn(1, 3, 640, 640) 

torch.onnx.export(model, dummy_input,  "checkpoints/model.onnx")