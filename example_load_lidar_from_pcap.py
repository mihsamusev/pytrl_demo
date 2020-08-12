from datasets.pcapframeparser import PcapFrameParser
from datetime import datetime
import numpy as np
import time
# visuals
import vispy
import open3d

fileName = "C:/Users/msa/Documents/datasets/CREATE lidar camera/lidardata/2019_07_08_13_07_38_to_14_10_54/pcap/2019-07-08-13-07-31_Velodyne-HDL-32-Data.pcap"
parser = PcapFrameParser(fileName)
gen = parser.generator()

pcd = open3d.PointCloud()
vis = open3d.Visualizer()
vis.create_window()
vis.add_geometry(pcd)
render_option = vis.get_render_option()
render_option.point_size = 0.01

to_reset_view_point = True
for i in range(20):
    (ts, frame) = next(gen)
    print(datetime.fromtimestamp(ts))
    x, y, z = frame.getCartesian()
    xyz = np.vstack([x,y,z]).T

    pcd.points = open3d.Vector3dVector(xyz)
    vis.update_geometry()
    if to_reset_view_point:
        vis.reset_view_point(True)
        to_reset_view_point = False
    vis.poll_events()
    vis.update_renderer()
    time.sleep(0.2)

vis.destroy_window()