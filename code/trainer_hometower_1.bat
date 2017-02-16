cd C:\opencv\build\x64\vc11\bin

opencv_traincascade -data "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\RESULTS\140326-1" -vec "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\positives.xml" -bg "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\bg.txt"  -numNeg 2000 -numPos 2300 -numStages 15 -precalcValBufSize 50000 -precalcIdxBufSize 50000 -featureType LBP -w 28 -h 28 -minHitRate 0.97 -maxFalseAlarmRate 0.4 -weightTrimRate 0.95 -maxDepth 1 maxWeakCount 20

PAUSE