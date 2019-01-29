#!/usr/bin/python

from Counter import linecounter as lc
from time import sleep
import cv2
import os
import easygui
 
archivosAEnviar=[]

fn = easygui.fileopenbox(default="/media/francisco/SiliconPowerArmor/SDM/",filetypes = ['*.avi','*.mp4'])
cam = cv2.VideoCapture(fn)
MAXW=700
mindist=200
ruta,ext=os.path.splitext(fn)

ruta2,nombredearchivo=os.path.split(fn)

dirpath = os.getcwd()
archsal=ruta+'.csv'


ret_val, imgFile2 = cam.read()

if not ret_val:
    print ('ERROR: no se pudo abrir la camara, saliendo')
    exit()



title  ="Cuantas lineas de conteo?"
msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
choices = ["1", "2", "3", "4", "5", "6"]
choice = easygui.choicebox(msg, title, choices)
type(choice)
lineasDeConteo=int(choice)
print "usted ha seleccionado ",lineasDeConteo," lineas de conteo"

contadores=[]
for cc in range(lineasDeConteo):
    lineaDeConteo=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo #' +str(cc+1),filename=archsal,linecount=cc+1)
    archivosAEnviar.append(lineaDeConteo.archivosalidajpg)
    contadores.append(lc.counter(lineaDeConteo.pt1,lineaDeConteo.pt2,filename=archsal,linecount=cc+1,fps=20))
    sleep(0.5)
    
for cnt in contadores:
    cnt.saveLine()
    archivosAEnviar.append(cnt.filename_output_line)
    archivosAEnviar.append(cnt.filename_output)
    


print ('Saliendo...')
cam.release()
