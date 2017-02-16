cd E:\Users\moydevma\opencv\build\x86\vc11\bin

set INFOFILE=E:\Users\moydevma\Thesis Data\Image Identification\HNM 1\pos\info.dat
set DESTINATIONFILE=E:\Users\moydevma\Thesis Data\Image Identification\HNM 1\pos\positives.xml
set /A D=24
set /A NUMSAMPLES=5680
opencv_createsamples -info "%INFOFILE%" -vec "%DESTINATIONFILE%" -w %D% -h %D% -num %NUMSAMPLES%

PAUSE