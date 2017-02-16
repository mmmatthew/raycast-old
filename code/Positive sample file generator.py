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

import cv2, sys, os, time, random, subprocess
import numpy as np
from scipy import ndimage
from osgeo import gdal, gdalconst, ogr

# File formats
driver = gdal.GetDriverByName('GTiff')
driver.Register()
driver_shp = ogr.GetDriverByName('ESRI Shapefile')
driver_shp.Register()

# Change Dir
os.chdir('E:/Users/moydevma/Thesis Data/Image Identification/')
# Check existence of img folders
if not os.path.exists('training images positive/img'):
    os.makedirs('training images positive/img')
if not os.path.exists('training images negative/img'):
    os.makedirs('training images negative/img')

# Script Variables
WindowSize = 1.6 # m
fn_points = "E:/Users/moydevma/Dropbox/Thesis/06 - Image Interpretation/Training Data Generation/positives.shp"
##fn_points = "SEsmall.csv"
fn_image = "Testing images/l1_mosaic_rgb.tif"
##fn_image = 'rgb.tif'
Variations = 1
SampleSize = 24
filenamesPos =''
filenamesNeg = ''

# Load points
##points = np.genfromtxt(fn_points, delimiter = ',') # Format is id, Xpos, Ypos
datasource = driver_shp.Open(fn_points, 0)

if datasource is None:
    print "Shapefile load FAILED"
    sys.exit(1)
else:
    print "Shapefile loaded successfully: " , fn_points

pointsLayer = datasource.GetLayer()
pointsnumber = pointsLayer.GetFeatureCount()
print 'Number of sewer inlets: ', pointsnumber

# User input: sewer type
CONST_SEWERTYPE = input("Which sewer type should used as positive example? (99 for all)")
# User input: number of variations
VariationsPos = input("How many variations should be generated for positive examples?")
# User input: number of variations
if CONST_SEWERTYPE <> 99:
    VariationsNeg = input("How many variations should be generated for negative examples?")

# Initiate points list
points = []

# Fill list from shapefile
for feature in pointsLayer:
    sewerType = feature.GetField('sewerType')
    geometry = feature.GetGeometryRef()
    sewerX = geometry.GetX()
    sewerY = geometry.GetY()
    points.append( [sewerType, sewerX, sewerY])

# Load image
StartTime = time.time()
geoimg = gdal.Open(fn_image, gdalconst.GA_ReadOnly) # Format is id, Xpos, Ypos
if geoimg == None:
    print "Image file load FAILED"
    sys.exit(1)
else:
    EndTime = time.time()
    print "Image file loaded successfully: " , fn_image, 'in ', str(EndTime-StartTime), ' seconds'
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
index = 1
countPos = 0
countNeg = 0
for point in points:
    # Determine if this is a positive example or a negative one
    if point[0] == CONST_SEWERTYPE or CONST_SEWERTYPE ==99:
        isPositive = True
        Variations = VariationsPos
    else:
        isPositive = False
        Variations = VariationsNeg

    # Make Window
    window_width = int(round(WindowSize/PXWIDTH[0]))
    window_height = abs(int(round(WindowSize/PXWIDTH[1])))
    window_origin_X = int((point[1]-ORIGIN[0])/PXWIDTH[0] - window_width/2)
    window_origin_Y = int((point[2]-ORIGIN[1])/PXWIDTH[1] - window_height/2)

    # read data as BGR
    imgList = [None]*BANDS
    for j in range(BANDS):
        imgList[BANDS-j-1] = bandList[j].ReadAsArray(window_origin_X, window_origin_Y,window_width,window_height)
    # merge channels
    imgRGB = cv2.merge((imgList[0],imgList[1],imgList[2]))
    #  Grayscale
    imgGRAY = cv2.cvtColor(imgRGB,cv2.COLOR_BGR2GRAY)

    # Create random variations of image
    for j in range(Variations):
        # Parameters for manipulating image data
        phi = random.uniform(1,1.2)
        rho = random.uniform(-40,20)
        alpha = random.uniform(0,360)
        # Mod image
        newImage = ndimage.rotate(phi*(imgGRAY+rho), alpha)

        #crop the image
        w=int(round(newImage.shape[0]/2))
        newSize = SampleSize/2
        newImage = newImage[(w-newSize):(w+newSize), (w-newSize):(w+newSize)]

        # Sometimes flip the image
        if(random.randint(0,1)):
            newImage = np.flipud(newImage)
##            newImage = array(newImage0,dtype=uint8)

        # Save image and write filename
        filename ='sample_'+str(index)+'-'+str(j)+'.jpg'
        if isPositive:
            countPos += 1
            cv2.imwrite('training images positive/img/'+filename, newImage)
            filenamesPos = filenamesPos + 'img/'+filename +'  1  0 0 ' +str(SampleSize)+' '+str(SampleSize) + '\n'
        else:
            countNeg += 1
            cv2.imwrite('training images negative/img/'+filename, newImage)
            filenamesNeg = filenamesNeg + 'img/'+filename + '\n'
    index += 1

print 'Images saved: ', countPos, ' positive and  ', countNeg, 'negatives'

# Save list of positive filenames
try:
    file = open("training images positive/info.dat", "r")
    filenamesPos = file.read() + '\n' + filenamesPos
    file.close
except:
    print 'creating new info.dat file'

file = open("training images positive/info.dat", "w")
file.write(filenamesPos)
file.close()

# Save list of negative filenames
try:
    file = open("training images negative/bg.txt", "r")
    filenamesPos = file.read() + '\n' + filenamesPos
    file.close
except:
    print 'creating new bg.txt file'

file = open("training images negative/bg.txt", "w")
file.write(filenamesNeg)
file.close()


# CREATE VEC FILE

# set variables
infofile = "E:\Users\moydevma\Thesis Data\Image Identification\training images positive\info.dat"
destinationfile = "E:\Users\moydevma\Thesis Data\Image Identification\training images positive\positives.xml"
d = '24'
numsamples = '4000'

#start subprocess
process = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE,stdout = subprocess.PIPE)
# change directory
process.stdin.write('cd E:\Users\moydevma\opencv\build\x86\vc11\bin')

# make vec file
command = 'opencv_createsamples -info %s -vec %s -w %s -h %s -num %s' % (infofile,destinationfile,d,d,numsamples)
process.stdin.write(command)



#END
EndTime = time.time()
print "Operation time: " ,  str(EndTime-StartTime), ' seconds'