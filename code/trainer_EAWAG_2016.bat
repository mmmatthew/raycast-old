C:
cd C:\opencv2\build\x86\vc12\bin

opencv_traincascade -data "E:\2014 - Moy de Vitry\Main Files\06 - Image Interpretation\Classifier Training\TEST_CLASSIFY" -vec "E:\2014 - Moy de Vitry\Main Files\06 - Image Interpretation\TRAINING FILES for first G classifier\positives.xml" -bg "E:\2014 - Moy de Vitry\Main Files\06 - Image Interpretation\TRAINING FILES for first G classifier\bg.txt"  -numNeg 2000 -numPos 2300 -numStages 15 -precalcValBufSize 48000 -precalcIdxBufSize 48000 -featureType LBP -w 28 -h 28 -minHitRate 0.99  -weightTrimRate 0.95 -maxDepth 2 maxWeakCount 20

PAUSE