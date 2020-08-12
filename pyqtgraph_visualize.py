import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph.ptime as ptime
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from datasets.folderimagereader import FolderImageReader
from datasets.pcapframeparser import PcapFrameParser

class ImageView(pg.ImageView):
    def __init__(self, generator, parent=None):
        super().__init__(parent)
        self.generator = generator
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.view = self.getView()

    def setLimits(self, data, margin=10):
        xmin, ymin = 0, 0
        xmax, ymax = data.shape[:2]
        #self.view.setLimits(xMin=xmin - margin, xMax=xmax + margin, 
            #yMin=ymin - margin, yMax=ymax + margin)
        self.view.setAspectLocked(lock=True, ratio=1)

    def setFrame(self, data):
        if data is not None:
            self.setImage(data, axes={'x':1, 'y':0, 'c':2})
            #self.setLimits(data)

    def nextFrame(self):
        ts, data = next(self.generator)
        self.setFrame(data)

class LidarView(gl.GLViewWidget):
    def __init__(self, generator, parent=None):
        super().__init__(parent)
        
        self.generator = generator
        # grid
        self.grid = gl.GLGridItem()
        self.grid.scale(1,1,1)
        self.addItem(self.grid)

        # axes and annotation
        self.axes = gl.GLAxisItem(glOptions="additive")
        self.addItem(self.axes)

        # cloud
        self.rawPoints = np.zeros((1,3))
        self.rawColor = np.zeros((1,3), dtype=np.float32)
        self.rawPtSize = 4
        self.rawCloud = gl.GLScatterPlotItem(
            pos=self.rawPoints,color=self.rawColor,size=self.rawPtSize)
        self.addItem(self.rawCloud)

    def setFrame(self, data):
        if data is None:
            self.rawPoints = np.zeros((1,3))
            self.rawColor = np.zeros((1,3), dtype=np.float32)
        else:
            self.rawPoints = data
            self.rawColor = np.zeros((data.shape[0],3), dtype=np.float32)
            self.rawColor[:,1] = 1
        #draw raw points
        self.rawCloud.setData(pos=self.rawPoints,
            color=self.rawColor,size=self.rawPtSize)

    def nextFrame(self):
        ts, frame = next(self.generator)
        x, y, z = frame.getCartesian()
        data = np.vstack([x,y,z]).T
        self.setFrame(data)

def get_main_window():
    # main window
    win = QtWidgets.QMainWindow()
    win.setMinimumSize(800,600)
    centralWidget = QtWidgets.QWidget()
    centralWidget.setMinimumSize(QtCore.QSize(400, 300))
    centralWidget.setStyleSheet("background-color: black;")
    win.setCentralWidget(centralWidget)
    win.show()
    return win

def update(iv, lv):
    # Queue next call to self
    QtCore.QTimer.singleShot(1, lambda: update(iv, lv))
   # iv.nextFrame()
    lv.nextFrame()

if __name__ == '__main__':
    import sys

    # lidar gen
    base_path = "C:/Users/msa/Documents/datasets/CREATE lidar camera/lidardata/2019_07_08_13_07_38_to_14_10_54/"
    lidar_file = base_path + "pcap/2019-07-08-13-07-31_Velodyne-HDL-32-Data.pcap"
    parser = PcapFrameParser(lidar_file)
    lidar_gen = parser.generator()
    
    # video gen
    video_folder = base_path + "img"
    fir = FolderImageReader(video_folder)
    video_gen = fir.generator()

    app = QtGui.QApplication(sys.argv)
    win = get_main_window()
    layout = QtGui.QGridLayout(win.centralWidget())

    # left widget
    iv = ImageView(video_gen)
    layout.addWidget(iv, 0, 0)
    iv.nextFrame()

    # right widget
    lv = LidarView(lidar_gen)
    layout.addWidget(lv, 0, 1)
    lv.nextFrame()

    update(iv, lv)

    sys.exit(app.exec())
