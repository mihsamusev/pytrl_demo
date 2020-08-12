from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.widgets.RawImageWidget import RawImageGLWidget
app = QtGui.QApplication([])

win = QtWidgets.QMainWindow()
win.setMinimumSize(800,600)
centralWidget = QtWidgets.QWidget()
centralWidget.setMinimumSize(QtCore.QSize(400, 300))
centralWidget.setStyleSheet("background-color: black;")
win.setCentralWidget(centralWidget)
win.show()
# get a layout
layoutgb = QtGui.QGridLayout(centralWidget)

glvw = gl.GLViewWidget()
z = pg.gaussianFilter(np.random.normal(size=(50,50)), (1,1))
p13d = gl.GLSurfacePlotItem(z=z, shader='shaded', color=(0.5, 0.5, 1, 1))
glvw.addItem(p13d)
layoutgb.addWidget(glvw, 0, 0)



## Create window with GraphicsView widget
glw = pg.GraphicsLayoutWidget()
glw.setWindowTitle('pyqtgraph example: ImageItem')
vv = glw.addViewBox()

## Create image item

data = np.random.normal(size=(15, 600, 600), loc=1024, scale=64).astype(np.uint16)
img = pg.ImageItem(data[0])
vv.addItem(img)

layoutgb.addWidget(glw, 0, 1)  ### uncommenting this line causes 
       # the plot widget to appear and the 3d widget to disappear

glw.sizeHint = lambda: pg.QtCore.QSize(100, 100)
glvw.sizeHint = lambda: pg.QtCore.QSize(100, 100)
glvw.setSizePolicy(glw.sizePolicy())

QtGui.QApplication.instance().exec_()