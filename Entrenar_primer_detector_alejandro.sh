#!/bin/bash
./darknet detector train data/obj.data yolo-obj.cfg darknet19_448.conv.23 -gpus 0,1,2,3,4 | tee resultados_entrenamiento.txt
