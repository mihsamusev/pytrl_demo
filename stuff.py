import torch
import numpy as np
from pathlib import Path
from google.protobuf import text_format
from second.protos import pipeline_pb2
from second.pytorch.builder import input_reader_builder
from second.pytorch.train import build_network, example_convert_to_torch

def main():
    cfg_path = Path('/..../pointpillars/car/xyres_##.config')
    ckpt_path = Path('/..../voxelnet-######.tckpt')

    config = pipeline_pb2.TrainEvalPipelineConfig()
    print("config reading")
    with open(cfg_path, "r") as f:
        proto_str = f.read()
        text_format.Merge(proto_str, config)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("building net")
    net = build_network(config.model.second).to(device).float().eval()
    net.load_state_dict(torch.load(ckpt_path))
    print("net built")

    eval_input_cfg = config.eval_input_reader
    dataset = input_reader_builder.build(
            eval_input_cfg,
            config.model.second,
            training=False,
            voxel_generator=net.voxel_generator,
            target_assigner=net.target_assigner).dataset
    idx = 0
    example = dataset[idx]

    example["coordinates"] = np.pad(
        example["coordinates"], ((0, 0), (1, 0)),
        mode='constant',
        constant_values=0)
    # don't forget to add newaxis for anchors
    example["anchors"] = example["anchors"][np.newaxis, ...]
    example_torch = example_convert_to_torch(example, device=device)

    voxels = example_torch["voxels"]
    num_points = example_torch["num_points"]
    coors = example_torch["coordinates"]
    batch_anchors = example["anchors"]
    batch_size_dev = batch_anchors.shape[0]

    voxel_features = net.voxel_feature_extractor(voxels, num_points, coors)
    spatial_features = net.middle_feature_extractor(voxel_features, coors, batch_size_dev)

    # Export the model
    print("exporting as onnx")
    torch_out = torch.onnx._export(net.rpn,
                                   (spatial_features),
                                   "rpn.onnx",
                                   export_params=True)
    print("export complete")
    
main()
