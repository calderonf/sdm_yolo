#!/usr/bin/python3
import cv2
import easygui
import glob
import numpy as np
import os
from math import floor
from math import ceil

def ajustarRecorte(roi,imagesizex=1920,imagesizey=1080):
    
    cx=roi[0]
    cy=roi[1]

    cw=roi[2]
    ch=roi[3]
    
    cu=cx+cw
    cv=cy+ch
    
    minimoy=0
    maximoy=imagesizey
    
    mintamx=854#854x480 is the minimun 16/9 relation of image standard
    mintamy=480
    
    maxtamx=imagesizex
    
    #print ("antes0", cx,", ",cu,", ",cy,", ",cv,", ",cw,", ",ch)
    
    incremento=20
    cx-=incremento
    cy-=incremento
    
    cu+=incremento
    cv+=incremento
    
    cw=abs(cu-cx)
    ch=abs(cv-cy)
    
    #print ("antes1", cx,", ",cu,", ",cy,", ",cv,", ",cw,", ",ch)
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
    
    if cw/ch>(1920/1080):
        #print ("ajusto por y")
        diffy=(cw*1080/1920)-ch
        cy=cy-int(floor(diffy/2.0))
        cv=cv+int(ceil(diffy/2.0))
        
    if cw/ch<(1920/1080):
        #print ("ajusto por w")
        diffx=(ch*1920/1080)-cw
        cx=cx-int(floor(diffx/2.0))
        cu=cu+int(ceil(diffx/2.0))
    #print(cw/ch)
        
    cw=abs(cu-cx)
    ch=abs(cv-cy)
    
    #print(cw/ch)
    
    #print ("durante", cx,", ",cu,", ",cy,", ",cv,", ",cw,", ",ch)
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
        
    if cx<0:
        cx=0
    if cy<0:
        cy=0
    if cu>=imagesizex:
        cu=imagesizex-1
    if cv>=imagesizey:
        cv=imagesizey-1
    cw=abs(cu-cx)
    ch=abs(cv-cy)
    #print ("despues", cx,", ",cu,", ",cy,", ",cv,", ",cw,", ",ch)
    return (cx,cy,cw,ch)


folder=easygui.diropenbox(title="Seleccione la carpeta con los videos a revisar",default="/media/francisco/monitoreo/pruebas/")

filelist=glob.glob(folder+"/*.mp4")
if len(filelist)==0:
    print("no hay archivos .mp4 intentando AVI")
    filelist=glob.glob(folder+"/*.avi")

if len(filelist)==0:
    print("no hya archivos de video, saliendo")
    exit()
filelist.sort()
print (filelist)
firstime=True
ErrorEnVideo=False
print("Listando ",str(len(filelist)),"Elementos")    
counterarchivos=1
numvideos=len(filelist)

if numvideos>100:
    alphaacum=0.001
    maxframes=20
if numvideos<=100:
    alphaacum=0.005
    maxframes=30
if numvideos<=10:
    alphaacum=0.01
    maxframes=30


for fn in filelist:
    ext=os.path.basename(fn)

    frames=0
    print("procesando archivo ",counterarchivos, " de ",str(len(filelist))) 
    counterarchivos+=1
    cam = cv2.VideoCapture(fn)
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR: no se pudo abrir el archivo de video guardando registro, intentando siguiente')
        with open(folder+"/"+"Error.txt","a") as f: 
            f.write("Error en archivo: "+fn+"\n")
            print("Error en video")
            ErrorEnVideo=True
        continue
    FPS=cam.get(cv2.CAP_PROP_FPS)
    TOTFRAMES=cam.get(cv2.CAP_PROP_FRAME_COUNT)
    while frames<maxframes:
        error=False
        frames+=1
        ret_val, imgFile2 = cam.read()
        if not ret_val:
            print ("no se pudo abrir el cuaro de video Error")
            with open(folder+"/"+"Error.txt","a") as f:  
                f.write("Error en capturar imagen del archivo: "+fn+"\n")
            error=True
            break
        if firstime:
            firstime=False
            accumulator = np.float32(imgFile2)
        cv2.accumulateWeighted(imgFile2,accumulator,alphaacum)#Filtro FIR alpha 1-alpha a 0.001 ya que trabaja con 30 imagenes y lo normal son 144 archivos total 4320 lo que crea un paso bajos a pi/4 mas o menos
      
    if not error:
        with open(folder+"/"+"Validos.txt","a") as f:  
            f.write(ext+",FPS:"+str(int(FPS))+",Total_Frames:"+str(int(TOTFRAMES))+",Duracion en seg:"+str(int(TOTFRAMES/FPS))+",Duracion en in min:"+str(int(round((TOTFRAMES/FPS)/60)))+"\n")
    cam.release()
    
res1 = cv2.convertScaleAbs(accumulator)
cv2.imwrite(folder+"/promedio.jpeg",res1)
if ErrorEnVideo:
    print("ERROR EN UNO DE LOS VIDEOS REVISAR......")
resmini=cv2.resize(res1,(854,480))
cv2.imshow("Requiere_ROI?",resmini)
cv2.waitKey(200)
res=easygui.boolbox(msg='Requiere de seleccion de ROI', title='ROI', choices=('[S]i', '[N]o'), default_choice='No', cancel_choice='No')
cv2.destroyWindow("Requiere_ROI?")
cv2.waitKey(2)
if res:
    print("Por Favor seleccione la ROI y oprima enter cuando este lista,\nse le mostrara de nuevo la roi seleccionada con los ajustes de relacion 16:9\nOprima Y para confirmar o cualquier otra para repetir...")
    repetir=True
    while repetir:
        img=cv2.imread(folder+"/promedio.jpeg")
        cv2.namedWindow("Oprima Enter cuando este listo")
        cv2.moveWindow("Oprima Enter cuando este listo",0,0)

        roi=cv2.selectROI("Oprima Enter cuando este listo",img)
        cv2.destroyAllWindows()
        img2=img.copy()
        #print (roi)
        roi2=ajustarRecorte(roi)
        cv2.rectangle(img, (roi2[0],roi2[1]), (roi2[0]+roi2[2],roi2[1]+roi2[3]),(255,255,255), 3,0)
        cv2.rectangle(img, (roi[0],roi[1]), (roi[0]+roi[2],roi[1]+roi[3]),(255,0,0), 3,0)
        cv2.namedWindow("oprima y si esta lista la roi")
        cv2.moveWindow("oprima y si esta lista la roi",0,0)
        cv2.imshow("oprima y si esta lista la roi",img)
        key=cv2.waitKey(0)&0xFF
        if key ==ord("y") or key == ord("Y"):
            repetir=False
    print ("ROI definitiva:",roi2)
    with open(folder+"/ROI.txt", "w") as f:
        f.write(str(roi2))
    """
    with open(folder+"/ROI.txt", "r") as f:
        data = f.readline()
    roi3=eval(data)
    print ("Data almacenada en str= ", data, "en tupla =", roi3)
    """
    
    cv2.destroyWindow("oprima y si esta lista la roi")
    
print ('Saliendo...')
#exit()
