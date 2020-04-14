#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:13:28 2019

@author: administrador
"""
import cv2
import datetime
import numpy as np
import darknet as dn
import threading
import Queue


net0 = dn.load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta0 = dn.load_meta("../data/obj.data")

net1 = dn.load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta1 = dn.load_meta("../data/obj.data")

def PredictThread(net,meta,img,out_queue):
    #imgcloned = np.array(img)
    imgFile3 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    tama=imgFile3.shape
    imgFileptr,cv_img=dn.get_iplimage_ptr(imgFile3)   
    imgFileptr=dn.copy_iplimage_ptr(imgFile3,imgFileptr,cv_img)
    imgImported=dn.make_image(tama[1],tama[0],tama[2])
    dn.ipl_in2_image(imgFileptr,imgImported)
    erre=dn.detect_img(net, meta, imgImported) 
    print (erre)
    out_queue.put(erre)



my_queue = Queue.Queue()
from Secretos.secrets import fn,fn1,fn2,fn3
cam = cv2.VideoCapture(fn3)

Tamx=720#1920
timedelta=4
Estado=1
while True:# se itera 5 segundo para estabilizar la conexion
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
    #if k==ord ("p" )or k==ord("P"):
    bucle=1
    while(bucle):
        if Estado==1:
            Estado=2
            bucle=0
            thread1 = threading.Thread(PredictThread(net0,meta0,imgFile2, my_queue)) 
            thread1.start()
        elif Estado==2:
            Estado=3
            bucle=0
            thread2 = threading.Thread(PredictThread(net1,meta1,imgFile2, my_queue)) 
            thread2.start()
        elif Estado==3:
            Estado=1
            bucle=1
            thread1.join()
            thread2.join()
        
cv2.destroyWindow('streaming')
cv2.destroyAllWindows()
cv2.waitKey(3)
cv2.waitKey(30)
cv2.waitKey(300)
exit()
