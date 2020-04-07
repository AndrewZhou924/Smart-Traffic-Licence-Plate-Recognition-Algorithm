import os
import cv2
print(os.path.exists('/data/OpenSourceDatasets/CCPD2019/ccpd_tilt/0700-40_41-386&303_592&587-592&587_389&415_386&303_589&475-19_16_28_25_8_29_25-133-227.jpg'))
img = cv2.imread('/data/OpenSourceDatasets/CCPD2019/ccpd_tilt/0700-40_41-386&303_592&587-592&587_389&415_386&303_589&475-19_16_28_25_8_29_25-133-227.jpg');
print(img)