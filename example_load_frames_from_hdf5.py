import cv2
from imutils.paths import list_images
import imutils
import re
import datetime

def get_frame_number(impath):
    return int(re.search(r"image data (\d+)", impath).group(1))

def get_timestamp(impath):
    "assuming that the timestamp is a part of the image name"
    date_str = impath.split(".")[0]
    date_str = re.split(r"image data \d+ ", date_str)[1]
    date = datetime.datetime.strptime(date_str, '%Y-%b-%d %H %M %S %f')
    return date

# Load the data
impaths = list(list_images("C:/Users/msa/Documents/datasets/CREATE lidar camera/ImageData/"))
impaths = sorted(impaths, key=get_frame_number)

for impath in impaths[:100]:
    date = get_timestamp(impath)
    print(date)
    image = cv2.imread(impath)
    image = imutils.resize(image, width=640)
    
    # do something cool

    cv2.imshow("im", image)
    cv2.waitKey(0)
  
#closing all open windows
cv2.destroyAllWindows()
'''
reader = dataset.hdf5generator(filepath)
for data in reader:
    # do something
    pass

reader = dataset.pcap_reader(filename, callib)
for data in reader:
    # do something
    pass

reader = dataset.ats_radar_reader(filename, callib)
for data in reader:
    # do something
    pass

# KITTI wih pykitti
basedir = '/home/dodo_brain/kitti_data/'
date = '2011_09_26'
drive = '0019'
data = pykitti.raw(basedir, date, drive, frames=range(0, 50, 5))
for cam0_image in data.cam0:
    # do something
    pass
'''