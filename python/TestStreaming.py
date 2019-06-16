#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:13:28 2019

@author: administrador
"""
import cv2
fn='rtsp://movil:egccol@186.29.90.163:8891/EGC'
cam = cv2.VideoCapture(fn)
MAXW=700
mindist=200

for nn in range(900):# se itera 5 segundo para estabilizar la conexion
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo')
        exit()
    cv2.imshow('streaming',imgFile2)
    cv2.waitKey(30)
cv2.destroyAllWindows()
cv2.waitKey(2)