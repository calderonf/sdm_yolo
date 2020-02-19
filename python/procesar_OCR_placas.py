#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 10:45:53 2020

@author: francisco
"""
import random
import cv2
import numpy as np


def compareCharacters(cra,crb,delta=2.0):
    cxa=cra[2][0]
    cxb=crb[2][0]
    distancia=abs(cxa-cxb)
    if distancia<delta:
        return True
    return False
def promedioAnchos(OCR):
    promedio=0
    for char in OCR:
        promedio+=char[2][2]
    return promedio/len(OCR)
def minorConfidence(cra,crb,i,j):
    if cra[1]>crb[1]:
        return j
    return i
def eliminarRepetidos(OCR,pceliminacion=0.2):
    """
    funcion que elimina los caracteres repetidos en las detecciones de OCR, si estas detecciones son muy cercanas 
    se eliminan la cercania esta dada por que tan juntas estan en su coordenada x
    se puede aumentar esta diferencia aumentando el PCeliminacion por ahora esta en 20%
    """
    if len(OCR)<=6:# Si tiene menos de 6 o 6 letras retorne la misma cadena de detecciones
        return OCR
    paraeliminar=[]
    promedio=promedioAnchos(OCR)
    for i in range(len(OCR)):
        for j in range(i + 1, len(OCR)):
            if compareCharacters(OCR[i], OCR[j],delta=promedio*pceliminacion):
                paraeliminar.append(minorConfidence(OCR[i], OCR[j],i,j))
    paraeliminar=list(set(paraeliminar))# quitar elementos repetidos
    for i in sorted(paraeliminar, reverse=True):
        if len(OCR)<=6:
            break
        del OCR[i]
    return OCR

def graficarPlacas(img,placa,resOCR,offset=(0,0),imwrite=False):
    #tomar las 6 mejores detecciones:
    #resOCR=resOCR[0:6]
    colour=(int(random.uniform(100,150)),int(random.uniform(180,255)),int(0))
    colour2=(int(random.uniform(180,255)),int(random.uniform(100,150)),int(0))
    x=placa[0]+offset[0]
    y=placa[1]+offset[1]
    w=placa[2]
    h=placa[3]
    u=x+w
    v=y+h
    resOCR.sort(key=lambda tup: tup[2][0])#organiza de izquierda a derecha las detecciones del OCR
    
    resOCR=eliminarRepetidos(resOCR)    
    
    #pintar deteccion de placa
    #cv2.rectangle(img, (x,y), (u,v),colour, thickness=2, lineType=8, shift=0)
    cstr=""
    for j in (range(len(resOCR))):
        cw=int(resOCR[j][2][2])
        ch=int(resOCR[j][2][3])
        cx=int(resOCR[j][2][0])-(cw/2)
        cy=int(resOCR[j][2][1])-(ch/2)
        cstr+=resOCR[j][0]
        
        xc=x+cx
        yc=y+cy
        uc=xc+cw
        vc=yc+ch
        #cv2.rectangle(imgFile2, (xc,yc), (uc,vc),colour2, thickness=1, lineType=8, shift=0)
        cv2.putText(img,str(resOCR[j][0]), (xc,vc+20), cv2.FONT_HERSHEY_SIMPLEX,0.6, colour2)
    
    cv2.putText(img,str(cstr), (x,y-4), cv2.FONT_HERSHEY_SIMPLEX,1, colour)
    cv2.imshow('VideoPLACA', img)
    cv2.waitKey(1)
    if imwrite:
        cv2.imwrite("../../imagen_capturada_PLACA_"+cstr+"_"+str(random.randint(10,99))+'.JPG',img)
    
    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
    return (cstr,(x,y-4))
    #if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
    #    print ('interrupcion de usuario...')

def recortarDeteccionConTexto(copiaimagen,textofecha,textocamara,textodireccion,cy,cv,cx,cu,cw,ch):
    font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.2, 1.1 ,0 ,1 ,cv2.cv.CV_AA)
    minimoy=152
    maximoy=1024
    
    mintamx=700
    mintamy=560
    
    maxtamx=1920
    incremento=40
    cx-=incremento
    cy-=incremento
    
    cu+=incremento
    cv+=incremento
    
    
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
        