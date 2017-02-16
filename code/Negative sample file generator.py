#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      moydevma
#
# Created:     12.03.2014
# Copyright:   (c) moydevma 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''Important: create file structure before running!'''

import cv2, sys, os, time, random
import numpy as np
from scipy import ndimage
from osgeo import gdal, gdalconst, ogr

# File formats
driver = gdal.GetDriverByName('GTiff')
driver.Register()
driver_shp = ogr.GetDriverByName('ESRI Shapefile')
driver_shp.Register()

# Script Variables
WindowSize = 28 # Pixels
#EAWAG
##fn_points = 'E:/Users/moydevma/Dropbox/Thesis/06 - Image Interpretation/Hard Negative Mining/Refreshed 2/results/2 Neighbors/misses.shp'
##fn_image = "E:/Users/moydevma/Thesis Data/Image Identification/Testing images/l1_clipped_rgb.tif"
##dstFolder= 'E:/Users/moydevma/Dropbox/Thesis/06 - Image Interpretation/Hard Negative Mining/Refreshed 2/results/2 Neighbors/'
##dstFolder="E:/Users/moydevma/Thesis Data/Image Identification/HNM 2/neg/"

#HOME
# fn_points = 'C:/Users/Matthew/Dropbox/Thesis/06 - Image Interpretation/Hard Negative Mining/Refreshed 3/negatives/neg_ref3.shp'
# fn_image = "S:/Master Thesis Data/05_Image Interpretation/Orthophotos/l1_clipped_rgb.tif"
# dstFolder="S:/Master Thesis Data/05_Image Interpretation/HNM 3/neg/"
# filenames =''

# Koeniz negatives
fn_points = "C:/Users/Matthew/Dropbox/Thesis/08 - Case Study/Koeniz/Classification Results/road_cadaster_50_100/3N/misses.shp"
fn_image = "S:/Master Thesis Data/08_Case Studies/Koeniz/Clipped orthophotos/koeniz_clipped_4cm.tif"
dstFolder="S:/Master Thesis Data/08_Case Studies/Koeniz/Negatives/"
filenames =''
# Load points
datasource = driver_shp.Open(fn_points, 0)

if datasource is None:
    print "Shapefile load FAILED"
    sys.exit(1)
else:
    print "Shapefile loaded successfully: " , fn_points

pointsLayer = datasource.GetLayer()
pointsnumber = pointsLayer.GetFeatureCount()
print 'Number of negative samples: ', pointsnumber

# Get points from shapefile
points =[]
for feature in pointsLayer:
    geometry = feature.GetGeometryRef()
    X = geometry.GetX()
    Y = geometry.GetY()
    points.append( [0, X, Y])

# Load image
StartTime = time.time()
geoimg = gdal.Open(fn_image, gdalconst.GA_ReadOnly) # Format is id, Xpos, Ypos
if geoimg == None:
    print "Image file load FAILED"
    sys.exit(1)
else:
    EndTime = time.time()
    print "Image file loaded successfully: " , fn_image
    CONST_IMDIM = (geoimg.RasterXSize, geoimg.RasterYSize)
    print "Dimensions: ", CONST_IMDIM

#Read image geoinfo
geotrf = geoimg.GetGeoTransform()
ORIGIN = (geotrf[0],geotrf[3])
PXWIDTH = (geotrf[1],geotrf[5])
BANDS = 3

# Define bands
bandList = [None]*BANDS
for j in range(BANDS):
    bandList[j] = geoimg.GetRasterBand(j+1) # 1-based index

#Process points
imgList = [None]*BANDS
index = 1
for point in points:

    # Make Window
    window_width = WindowSize
    window_height = WindowSize
    window_origin_X = int((point[1]-ORIGIN[0])/PXWIDTH[0] - window_width/2)
    window_origin_Y = int((point[2]-ORIGIN[1])/PXWIDTH[1] - window_height/2)

    # Make sure window is within image
    if min(window_origin_X,window_origin_Y)>=0 and min(CONST_IMDIM[0]-window_origin_X,CONST_IMDIM[1]-window_origin_Y)>=window_height:
        # read data as BGR
        for j in range(BANDS):
            imgList[BANDS-j-1] = bandList[j].ReadAsArray(window_origin_X, window_origin_Y,window_width,window_height)
        # merge channels
        imgRGB = cv2.merge((imgList[0],imgList[1],imgList[2]))
        #  Grayscale
        imgGRAY = cv2.cvtColor(imgRGB,cv2.COLOR_BGR2GRAY)

        # Save image and write filename
        filename ='sample_'+str(index)+'.jpg'
        cv2.imwrite(dstFolder+'img/'+filename, imgGRAY)
        filenames = filenames+ 'img/'+filename +'\n'
        index += 1
        if index % 100==0:
            time.sleep(0.05)
            print '.',

print index-1, ' images saved'
file = open(dstFolder+"bg.txt", "w")
file.write(filenames)
file.close()
EndTime = time.time()
print "Operation time: " ,  str(EndTime-StartTime), ' seconds'
