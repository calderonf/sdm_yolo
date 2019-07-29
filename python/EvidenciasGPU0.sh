#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
FECHA=`date +%Y%m%d`

if [ -d "/VideosSDM/$FECHA" ]; then
 # Control will enter here if $DIRECTORY exists.
 echo "El directorio existe"
else
 #si no existe el archivo
 echo "El directorio NO existe creandolo"
 mkdir '/VideosSDM/$FECHA'
fi

cd  /home/administrador/sdm_yolo/python
touch pyptaxi.data
rm pyptaxi.data

python2 PicoYPlacaYCebraStreaming.py

