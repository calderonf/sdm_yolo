#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 20:02:46 2019

@author: administrador
"""
import cv2
import time
from time import strftime
#import copy creo que no es necesario usar copy, ya cv2.copy hace un deep copy no una simple referencia. 

class recordVideo:
    def __init__(self, filename,Segundafoto,TTL=30,FPS=20,res=(1920,1080),dec=10,segev=5):
        """
        Funcion para inicializar estructura de grabador de video, 
        filename es el nombre del video a guardar
        TTL es el tiempo en segundos a guardar
        FPS son los cuadros por segundo
        res es la resolución del video
        """
        self.filename=filename
        self.segundafoto=Segundafoto
        self.cuadrosAGuardar=(TTL*FPS)+1
        self.CuadrosGuardados=self.cuadrosAGuardar
        self.dec=dec
        self.timea=time.time()
        
        self.contadorsegundafoto=segev
        
        self.fourcc = cv2.cv.CV_FOURCC('M','P','4','V')#('M','P','4','V') o ('M','J','P','G')
        self.out = cv2.VideoWriter(filename, self.fourcc, FPS/dec, res)
        
        self.finalizado=False
        self.guardadaSegFoto=False
        
        
        
    def SalvarCuadroVideo(self,cuadro):
        try:
            self.CuadrosGuardados-=1
            lapso=abs(time.time()-self.timea)
            
            if (self.CuadrosGuardados%self.dec)==0:
                self.out.write(cuadro)
            
            if (lapso>self.contadorsegundafoto) and (not self.guardadaSegFoto):
                #print ("Lapso = ",lapso,"contador= ",self.contadorsegundafoto)
                cv2.imwrite(self.segundafoto,cuadro)
                self.guardadaSegFoto=True
                #print("guardando foto a los ",abs(time.time()-self.timea)," segundos.")
            
            if self.CuadrosGuardados<=0 and (not self.finalizado):
                print("Video: ",self.filename," Salvado")
                self.out.release()
                self.finalizado=True
                return
        except:
            print("Error detectado en grabacion")
    
class grabadorVideos:
    def __init__(self,cuadrosnocausales=60,TTL=30):
        """
        Clase para grabar multiples videos  independientes al tiempo
        """
        self.videos=[]
        self.arreglocuadros=[]
        self.TAMMAX=cuadrosnocausales
        self.fpsingnore=10
        self.count=0
        self.TTL=TTL
        
    def nuevoVideo(self,filename,Segundafoto,TTL=50,FPS=20,res=(1920,1080),dec=10):
        self.TTL=TTL
        self.videos.append(recordVideo(filename,Segundafoto,TTL=self.TTL,FPS=FPS,res=res,dec=dec))
        for cant in self.arreglocuadros:
            self.videos[-1].out.write(cant)
        
    
    def procesarCuadro(self,cuadro):
        
        if ((self.count % self.fpsingnore)==0):
            self.arreglocuadros.append(cuadro.copy())
        
        if len (self.arreglocuadros)>self.TAMMAX:
            self.arreglocuadros.pop(0)
            
        self.count+=1
        
        if len(self.videos)>=0:
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
    
    grabar=grabadorVideos()
    cont=1
    while True:# se itera 5 segundo para estabilizar la conexion
        ret_val, imgFile2 = cam.read()
        if not ret_val:
            print ('ERROR:  no se pudo abrir la camara, saliendo')
            break
        cv2.imshow('streaming',imgFile2)
        grabar.procesarCuadro(imgFile2)
        k = cv2.waitKey(10)& 0xFF
        if k==ord('s') or k==ord('S'):
            print("Salvando Video",cont)
            grabar.nuevoVideo("videoEjemplo_"+"_t_"+str(strftime("%d%m%y_%H-%M-%S"))+"_"+str(cont)+".avi","fotoEjemplo"+str(cont)+"_t_"+str(strftime("%d%m%y_%H-%M-%S"))+".jpg")
            cont+=1
            
        if k==ord('q') or k==ord('Q'):
            break
    cv2.destroyWindow('streaming')
    cv2.destroyAllWindows()
    cv2.waitKey(3)
    cv2.waitKey(30)
    cv2.waitKey(300)

        