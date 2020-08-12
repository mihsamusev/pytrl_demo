import onnx2keras
from onnx2keras import onnx_to_keras
import keras
import onnx

path = "C:/Users/msa/Documents/datasets/pretrained architectures/PointPillars/pfe.onnx"
onnx_model = onnx.load(path)
k_model = onnx_to_keras(onnx_model)
print(k_model)
