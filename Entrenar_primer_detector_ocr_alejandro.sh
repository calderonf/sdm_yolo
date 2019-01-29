#!/bin/bash
#esto es un comentario... la primera linea se llama shebang. es pata que sepa que interprete de scrip usar. 
./darknet detector train data/OCR.data yolo-OCR.cfg darknet19_448.conv.23 -gpus 6
#./darknet detector train data/OCR.data yolo-OCR.cfg backup_OCR/yolo-OCR_50000.weights -gpus 7
