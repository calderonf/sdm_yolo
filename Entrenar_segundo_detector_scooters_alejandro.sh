#!/bin/bash
#esto es un comentario... la primera linea se llama shebang. es para que sepa que interprete de scrip usar. 
./darknet detector train data/SCOOTERS.data yolo-SCOOTERS.cfg darknet19_448.conv.23 -gpus 4,5,6,7
#Ejemplo, lo detuve en la iteracion 51000 y quiero que continue desde ahi>
#./darknet detector train data/PLACAS.data yolo-PLACAS.cfg backup_PLACAS/yolo-PLACAS_51000.weights  -gpus 6

