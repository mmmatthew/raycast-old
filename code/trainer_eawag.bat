cd E:\Users\moydevma\opencv\build\x86\vc11\bin

opencv_traincascade -data "E:\Users\moydevma\Dropbox\Thesis\06 - Image Interpretation\RESULTS\140326-4" -vec "E:\Users\moydevma\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\positives.xml" -bg "E:\Users\moydevma\Dropbox\Thesis\06 - Image Interpretation\TRAINING FILES\bg.txt"  -numNeg 2000 -numPos 2300 -numStages 15 -precalcValBufSize 12000 -precalcIdxBufSize 12000 -featureType LBP -w 28 -h 28 -minHitRate 0.99  -weightTrimRate 0.95 -maxDepth 1 maxWeakCount 20

PAUSE