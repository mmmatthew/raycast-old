cd C:\opencv\build\x64\vc11\bin

opencv_traincascade -data "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\RESULTS\140326-3" -vec "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\positives.xml" -bg "C:\Users\Matthew\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\bg.txt"  -numNeg 2000 -numPos 2300 -numStages 15 -precalcValBufSize 48000 -precalcIdxBufSize 48000 -featureType LBP -w 28 -h 28 -minHitRate 0.99  -weightTrimRate 0.95 -maxDepth 2 maxWeakCount 20

PAUSE