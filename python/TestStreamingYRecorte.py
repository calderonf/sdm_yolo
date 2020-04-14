#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:13:28 2019

@author: administrador
"""
import cv2
from Secretos.secrets import fn,fn1,fn2,fn3
import numpy as np
from math import floor, ceil
import datetime


def recortarDeteccionConTexto(copiaimagen,textofecha,textocamara,textodireccion,cy,cv,cx,cu,cw,ch):
    font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.2, 1.1 ,0 ,1 ,cv2.cv.CV_AA)
    minimoy=152
    maximoy=1024
    
    mintamx=640
    mintamy=512
    
    maxtamx=1920
    
    cw=abs(cu-cx)
    ch=abs(cv-cy)
    print ("antes", cy,", ",cv,", ",cx,", ",cu,", ",cw,", ",ch)
    #si es mas pequeño que la minima imagen aumente el tamaño total de la imagen
    if cw<mintamx:
        diffx=mintamx-cw
        cx=cx-int(floor(diffx/2.0))
        cu=cu+int(ceil(diffx/2.0))
        
    if ch<mintamy:
        diffy=mintamy-ch
        cy=cy-int(floor(diffy/2.0))
        cv=cv+int(ceil(diffy/2.0))
        
    cw=abs(cu-cx)
    ch=abs(cv-cy)
    print ("durante", cy,", ",cv,", ",cx,", ",cu,", ",cw,", ",ch)
    #si se pasa por arriba baje toda la imagen
    if cy<minimoy:
        diffy=minimoy-cy
        cy=cy+diffy
        cv=cv+diffy
    #si se pasa por abajo suba toda la imagen
    if cv>maximoy:
        diffy=cv-maximoy
        cy=cy-diffy
        cv=cv-diffy
        
    #si se pasa por izquierda corra a derecha toda la imagen
    if cx<0:
        diffx=-cx
        cx=cx+diffx
        cu=cu+diffx
    #si se pasa por derecha corra a izquierda toda la imagen
    if cu>maxtamx:
        diffx=cu-maxtamx
        cx=cx-diffx
        cu=cu-diffx
    # Ultimas 4 verificaciones por si acaso se pasa
    if cx<0:
        diffx=-cx
        cx=cx+diffx
    if cu>maxtamx:
        diffx=cu-maxtamx
        cu=cu-diffx
    if cy<minimoy:
        diffy=minimoy-cy
        cy=cy+diffy
    if cv>maximoy:
        diffy=cv-maximoy
        cv=cv-diffy
    cw=abs(cu-cx)
    ch=abs(cv-cy)
    print ("despues", cy,", ",cv,", ",cx,", ",cu,", ",cw,", ",ch)
    img=copiaimagen[cy:cv,cx:cu]
    imgaa=np.ascontiguousarray(img)
    
    sizex1=240+5
    sizey1=30
    cv2.cv.PutText(cv2.cv.fromarray(imgaa), textofecha, (cw-sizex1,sizey1), font, (255,255,255))
    
    sizex2=300+5
    sizey2=65
    cv2.cv.PutText(cv2.cv.fromarray(imgaa), textocamara, (cw-sizex2,sizey2), font, (255,255,255))
    
    sizex3=(3+4)
    sizey3=ch-(6+4)
    cv2.cv.PutText(cv2.cv.fromarray(imgaa), textodireccion, (sizex3,sizey3), font, (255,255,255))
    
    return imgaa
        
        
        
    
    
    
    
    
    
    

boxes = []
global estado
estado=1

def on_mouse(event, x, y, flags, params):
    global estado
    if event == cv2.cv.CV_EVENT_LBUTTONDOWN and estado==1:
        estado=2
        print ('Start Mouse Position: '+str(x)+', '+str(y))
        sbox = [x, y]
        boxes.append(sbox)

    if event == cv2.cv.CV_EVENT_LBUTTONUP and estado==2:
        estado=1
        print ('End Mouse Position: '+str(x)+', '+str(y))
        ebox = [x, y]
        boxes.append(ebox)
        


cam = cv2.VideoCapture(sr.fn)

cv2.namedWindow('streaming')

while True:# se itera 5 segundo para estabilizar la conexion
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo')
        break
    cv2.imshow('streaming',imgFile2)
    k = cv2.waitKey(1) & 0xFF
    if k==ord('q') or k==ord('Q'):
        break
    if k==ord('r') or k==ord('R'):
        
        cv2.imshow('recortar',imgFile2)
        k = cv2.waitKey(30) & 0xFF
        cv2.cv.SetMouseCallback('recortar', on_mouse, 0)
        while len(boxes)<2:
            k=cv2.waitKey(30) & 0xFF
        print ("seleccionados los dos puntos del rectangulo...")
        textofecha="2019-08-25 13:25:12"
        textocamara="CGT036 EXT2016 NVR2 CH11"
        textodireccion="AK 7 X CL 45"
        pt2=boxes.pop()
        pt1=boxes.pop()
        cy=min(pt1[1],pt2[1])
        cv=max(pt1[1],pt2[1])
        cx=min(pt1[0],pt2[0])
        cu=max(pt1[0],pt2[0])
        cw=abs(cu-cx)
        ch=abs(cv-cy)
        imgFile=recortarDeteccionConTexto(imgFile2,textofecha,textocamara,textodireccion,cy,cv,cx,cu,cw,ch)
        cv2.imshow('recorte final',imgFile)
        k = cv2.waitKey(0) & 0xFF
    
    
    
cv2.destroyWindow('streaming')
cv2.destroyAllWindows()
cv2.waitKey(3)
cv2.waitKey(30)
cv2.waitKey(300)
