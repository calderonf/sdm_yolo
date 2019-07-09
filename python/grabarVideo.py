#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 20:02:46 2019

@author: administrador
"""
import numpy as np
import cv2

class recordVideo:
    def __init__(self, filename,TTL=60,FPS=20,res=(1920,1080)):
        """
        Funcion para inicializar estructura de grabador de video, 
        filename es el nombre del video a guardar
        TTL es el tiempo en segundos a guardar
        FPS son los cuadros por segundo
        res es la resolución del video
        """
        self.filename=filename
        self.cuadrosAGuardar=TTL*FPS
        self.CuadrosGuardados=self.cuadrosAGuardar
        
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter(filename, self.fourcc, FPS, res)
        
        self.finalizado=False
        
    def SalvarCuadroVideo(self,cuadro):
        try:
            self.out.write(cuadro)
            self.CuadrosGuardados-=1
            
            if self.CuadrosGuardados<=0:
                print("Video: ",self.filename," Salvado")
                self.out.release()
                self.finalizado=True
                return
        except:
            print("Error detectado en grabacion")
    
class grabadorVideos:
    def __init__(self):
        """
        Clase para grabar multiples videos  independientes al tiempo
        """
        self.videos=[]
        
    def nuevoVideo(self,filename,TTL=60,FPS=20,res=(1920,1080)):
        self.videos.append(recordVideo(filename,TTL=TTL,FPS=FPS,res=res))
    
    def procesarCuadro(self,cuadro):
        if len(self.videos>=0)
            for video in self.videos:
                video.SalvarCuadroVideo(cuadro)
            for i in range(len(self.videos)-1,-1,-1):
                if self.videos[i].finalizado:
                    del self.videos[i]
                    


if __name__ == "__main__":
    fn='rtsp://movil:egccol@186.29.90.163:8891/EGC'
    fn2='rtsp://multiview:egccol@186.29.90.163:8891/Multiview'
    fn3='rtsp://movil:egccol@186.29.90.163:8891/CamFull2'
    cam = cv2.VideoCapture(fn)
    
    grabar=grabadorVideos
    cont=1
    while True:# se itera 5 segundo para estabilizar la conexion
        ret_val, imgFile2 = cam.read()
        if not ret_val:
            print ('ERROR:  no se pudo abrir la camara, saliendo')
            break
        cv2.imshow('streaming',imgFile2)
        grabar.procesarCuadro(imgFile2)
        k = cv2.waitKey(1)& 0xFF
        if k==ord('s') or k==ord('S'):
            print("Salvando Video",cont)
            grabar.nuevoVideo("videoEjemplo"+str(cont)+".avi")
            cont+=1
            
        if k==ord('q') or k==ord('Q'):
            break
    cv2.destroyWindow('streaming')
    cv2.destroyAllWindows()
    cv2.waitKey(3)
    cv2.waitKey(30)
    cv2.waitKey(300)

        