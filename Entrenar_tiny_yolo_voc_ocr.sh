#!bin/bash
#./darknet detector train cfg/tinyocr.data cfg/tiny-yolo-voc-ocr.cfg darknet19_448.conv.23
./darknet detector train cfg/tinyocr.data cfg/tiny-yolo-voc-ocr.cfg backupocr/tiny-yolo-voc-ocr_11000.weights
