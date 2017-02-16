cd C:\opencv\build\x64\vc12\bin

opencv_traincascade -data "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\RESULTS" -vec "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\positives.xml" -bg "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\bg.txt" -numPos 2000 -numNeg 2840 -numStages 20 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -featureType LBP -w 24 -h 24 -minHitRate 0.97 -maxFalseAlarmRate 0.4 -weightTrimRate 0.95 -maxDepth 1 maxWeakCount 20

PAUSE