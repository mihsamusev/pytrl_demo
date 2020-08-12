# import the necessary packages
import cv2
from imutils.paths import list_images
import imutils
import re
from datetime import datetime

def get_frame_number(impath):
    return int(re.search(r"image data (\d+)", impath).group(1))

def get_timestamp(impath):
    "assuming that the timestamp is a part of the image name"
    date_str = impath.split(".")[0]
    date_str = re.split(r"image data \d+ ", date_str)[1]
    date = datetime.strptime(date_str, '%Y-%b-%d %H %M %S %f')
    ts = datetime.timestamp(date)
    return ts

class FolderImageReader:
    def __init__(self, folder_name, frame_num_fun=None, timestamp_fun=None):
        self.frame_num_fun = frame_num_fun
        self.timestamp_fun = timestamp_fun
        if self.frame_num_fun is None:
            self.frame_num_fun = get_frame_number
        if self.timestamp_fun is None:
            self.timestamp_fun = get_timestamp

        impaths = list(list_images(folder_name))
        self.impaths = sorted(impaths, key=self.frame_num_fun)

    def generator(self):
        for p in self.impaths:
            ts = self.timestamp_fun(p)
            data = cv2.imread(p)
            yield (ts, data)



