import cv2
from imutils.paths import list_images
import imutils
import re
import datetime
from datasets.hdf5datasetwriter import HDF5DatasetWriter
import progressbar

def get_frame_number(impath):
    return int(re.search(r"image data (\d+)", impath).group(1))

def get_timestamp(impath):
    "assuming that the timestamp is a part of the image name"
    date_str = impath.split(".")[0]
    date_str = re.split(r"image data \d+ ", date_str)[1]
    date = datetime.datetime.strptime(date_str, '%Y-%b-%d %H %M %S %f')
    return date

# Load the data, sort by frame number
basePath = "D:/create lidar trafik data/newer data/ImageData/"
impaths = list(list_images(basePath))
impaths = sorted(impaths, key=get_frame_number)

print("[INFO] building HDF5 dataset...")
outputPath = basePath + "frames.hdf5"
writer = HDF5DatasetWriter((len(impaths), 360, 640, 3), outputPath)

# initialize the progress bar
widgets = ["Building Dataset: ", progressbar.Percentage(), " ",
progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval=len(impaths),
widgets=widgets).start()

for i, impath in enumerate(impaths):
    date = get_timestamp(impath)
    ts = (date - datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1)
    
    image = cv2.imread(impath)
    image = imutils.resize(image, width=640)
    writer.add([image], [ts])
    pbar.update(i)

# close the HDF5 writer
pbar.finish()
writer.close()