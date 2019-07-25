#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:13:28 2019

@author: administrador
"""
import cv2
fn='rtsp://movil:egccol@186.29.90.163:8891/EGC'
fn2='rtsp://multiview:egccol@186.29.90.163:8891/Multiview'
fn3='rtsp://movil:egccol@186.29.90.163:8891/CamFull2'
cam = cv2.VideoCapture(fn3)



while True:# se itera 5 segundo para estabilizar la conexion
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo')
        break
    cv2.imshow('streaming',imgFile2)
    k = cv2.waitKey(1)& 0xFF
    if k==ord('q') or k==ord('Q'):
        break
cv2.destroyWindow('streaming')
cv2.destroyAllWindows()
cv2.waitKey(3)
cv2.waitKey(30)
cv2.waitKey(300)
