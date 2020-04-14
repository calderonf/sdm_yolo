#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:13:28 2019

@author: administrador
"""
import cv2
import datetime

from Secretos.secrets import fn,fn1,fn2,fn3
cam = cv2.VideoCapture(fn)

Tamx=720#1920
timedelta=0
frames=100

while frames:# se itera 5 segundo para estabilizar la conexion
    frames-=1
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo')
        break
    
    
    ahora=datetime.datetime.now()
    fechaformatotexto=ahora.strftime("Server %d-%m-20%y %H_%M_%S")
    sizex1=50+5
    sizey1=130
    cv2.putText(imgFile2, fechaformatotexto, (Tamx-sizex1,sizey1), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255))
    
    antecitos=ahora-datetime.timedelta(seconds=timedelta)
    fechaformatotexto=antecitos.strftime("timedelta"+str(timedelta)+" %d-%m-20%y %H_%M_%S")
    sizex1=50
    sizey1=65
    cv2.putText(imgFile2, fechaformatotexto, (Tamx-sizex1,sizey1), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255))
    cv2.imshow('streaming',imgFile2)
    k = cv2.waitKey(1)& 0xFF
    if k==ord('q') or k==ord('Q'):
        break
    if k==ord('t') or k==ord('T'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
        timedelta+=1
        print ('timedelta en ',timedelta)
    if k==ord('m') or k==ord('M'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
        timedelta-=1
        print ('timedelta en ',timedelta)
cv2.destroyWindow('streaming')
cv2.destroyAllWindows()
cv2.waitKey(3)
cv2.waitKey(30)
cv2.waitKey(300)
exit()
