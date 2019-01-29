#!/bin/bash
#./darknet detector test cfg/tinyocr.data cfg/tiny-yolo-voc-ocr.cfg backupocr/tiny-yolo-voc-ocr_final.weights  ../ocr/000000000-+EQ+8D-239635_124430.png -tresh 0
#./darknet detector test cfg/tinyocr.data cfg/tiny-yolo-voc-ocr-predict.cfg backupocr/tiny-yolo-voc-ocr_10000.weights  ../ocr/000000000-+EQ+8D-239635_124430.png -tresh 0.02
#./darknet detector test cfg/voc.data cfg/tiny-yolo-voc.cfg tiny-yolo.weights  data/person.jpg

./darknet detector test cfg/tinyocr.data cfg/tiny-yolo-voc-ocr-predict.cfg backupocr/tiny-yolo-voc-ocr_39000.weights ../ocr/000000000-+EQ+8D-239635_124430.png  -tresh 0.02
