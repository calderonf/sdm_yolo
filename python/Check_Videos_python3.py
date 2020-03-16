#!/usr/bin/python3
import cv2
import easygui
import glob
import matplotlib.pyplot as plt
import numpy as np
import os

folder=easygui.diropenbox(title="Seleccione la carpeta con los videos a revisar",default="/media/francisco/monitoreo/27022020/27022020/27022020_KR50XCL5CSD100_0000/")

filelist=glob.glob(folder+"/*.mp4")
firstime=True
print("Aforando ",str(len(filelist)),"Elementos")    
counterarchivos=1
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
        continue
    FPS=cam.get(cv2.CAP_PROP_FPS)
    TOTFRAMES=cam.get(cv2.CAP_PROP_FRAME_COUNT)
    while frames<30:
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
        cv2.accumulateWeighted(imgFile2,accumulator,0.001)#Filtro FIR alpha 1-alpha a 0.001 ya que trabaja con 30 imagenes y lo normal son 144 archivos total 4320 lo que crea un paso bajos a pi/4 mas o menos
      
    if not error:
        with open(folder+"/"+"Validos.txt","a") as f:  
            f.write(ext+",FPS:"+str(int(FPS))+",Total_Frames:"+str(int(TOTFRAMES))+",Duration in seg:"+str(int(TOTFRAMES/FPS))+",Duration in min:"+str(int(round((TOTFRAMES/FPS)/60)))+"\n")
    cam.release()
    
res1 = cv2.convertScaleAbs(accumulator)
cv2.imwrite(folder+"/promedio.jpeg",res1)
plt.imshow(cv2.cvtColor(res1, cv2.COLOR_BGR2RGB))
    
print ('Saliendo...')
#exit()
