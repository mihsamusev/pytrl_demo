import cv2
from imutils.paths import list_images
import imutils
import re
import datetime
import matplotlib.pyplot as plt
from datasets.folderimagereader import FolderImageReader
def get_frame_number(impath):
    return int(re.search(r"image data (\d+)", impath).group(1))

def get_timestamp(impath):
    "assuming that the timestamp is a part of the image name"
    date_str = impath.split(".")[0]
    date_str = re.split(r"image data \d+ ", date_str)[1]
    date = datetime.datetime.strptime(date_str, '%Y-%b-%d %H %M %S %f')
    return date

# Load the data
SHOW_METHOD = "matplotlib"
folder_name = "C:/Users/msa/Documents/datasets/CREATE lidar camera/lidardata/2019_07_08_13_07_38_to_14_10_54/img"
impaths = list(list_images(folder_name))
impaths = sorted(impaths, key=get_frame_number)

fir = FolderImageReader(folder_name,
    timestamp_fun=get_timestamp, frame_num_fun=get_frame_number)

ax = None
for i in range(20):
    (ts, image) = next(fir.generator())
    print(ts)
    image = imutils.resize(image, width=640)
    
    # do something cool
    if SHOW_METHOD == "opencv":
        cv2.imshow("im", image)
        cv2.waitKey(0)
    elif SHOW_METHOD == "matplotlib":
        image = imutils.opencv2matplotlib(image)
        if ax is None: 
            ax = plt.imshow(image)
        else:
            ax.set_data(image)
        plt.pause(.1)
        plt.draw()

#closing all open windows
if SHOW_METHOD == "opencv":
    cv2.destroyAllWindows()