import numpy as np
import cv2
import imutils
from datasets.folderimagereader import FolderImageReader

# callib matix and distortion coeff
wcal, hcal = 1600, 1200 
mtx = np.array([
    [1.7473845059199218e+03, 0, 800],
    [0, 1.7523330232672765e+03, 600],
    [0, 0, 1]])
dist = np.array(
    [1.0558825619798969e-01, -1.2250501555283355e+00, 0, 0, 4.2302514361517840e+00])

# get image
base_path = "C:/Users/msa/Documents/datasets/CREATE lidar camera/lidardata/2019_07_08_13_07_38_to_14_10_54/"    
video_folder = base_path + "img"
fir = FolderImageReader(video_folder)
video_gen = fir.generator()
ts, img = next(video_gen)
h,  w = img.shape[:2]

# cam matrix
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(wcal,hcal))
print(newcameramtx)
print(roi)

# undistort
#dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
#x,y,w,h = roi
#dst = dst[y:y+h, x:x+w]
dst = imutils.resize(dst, 800)
cv2.imshow("undistorted", dst)

ori = imutils.resize(img, width=800)
cv2.imshow("ori", ori)

cv2.waitKey(0)
cv2.destroyAllWindows()