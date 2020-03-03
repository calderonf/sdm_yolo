#!/usr/bin/python2
from darknet import *
from Counter import linecounter as lc
from Track import tracking as tr
from time import sleep
import cv2
import os
import easygui
 
"""
#YOLO VOC
net = load_net("../cfg/yolo-voc.cfg", "../../darknet/yolo-voc.weights", 0)
meta = load_meta("../cfg/voc_py.data")
"""

#NUESTRO YOLO ENTRENADO 80000 iteraciones
net = load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta = load_meta("../data/obj.data")


"""
#YOLO COCO
net = load_net("yolo.cfg", "../../darknet/yolo.weights", 0)
meta = load_meta("coco_es.data")
"""
#primera vez
charlador=False
pintarTrayectos=True
framesttl=5
deCamara=False
MAXW=550 ## 200 pixeles maximo de ancho permitido
mindist=10

if deCamara:
    cam = cv2.VideoCapture(0)
else: 
    fn = easygui.fileopenbox(default="/media/francisco/SiliconPowerArmor/SDM/",filetypes = ['*.avi','*.mp4'])
    cam = cv2.VideoCapture(fn)
    MAXW=700
    mindist=200
    ruta,ext=os.path.splitext(fn)
    archsal=ruta+'.csv'

frames=0
ret_val, imgFile2 = cam.read()
frames+=1
if not ret_val:
    print ('no se pudo abrir la camara, saliendo')
    exit()

imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
tama=imgFile2.shape
imgImported=make_image(tama[1],tama[0],tama[2])

imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
ipl_in2_image(imgFileptr,imgImported)
rgbgr_image(imgImported)

track=tr.tracking(verbose=charlador,mindist=mindist,framesttl=framesttl)#verbose=False,mindist=100


title  ="Cuantas lineas de conteo?"
msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
choices = ["0","1", "2", "3", "4", "5", "6"]
choice = easygui.choicebox(msg, title, choices)
type(choice)
lineasDeConteo=int(choice)
print "usted ha seleccionado ",lineasDeConteo," lineas de conteo"

contadores=[]
for cc in range(lineasDeConteo):
    sleep(1)
    lineaDeConteo=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo' +str(cc+1),filename=archsal,linecount=cc+1)
    sleep(1)
    contadores.append(lc.counter(lineaDeConteo.pt1,lineaDeConteo.pt2,filename=archsal,linecount=cc+1,fps=20))


#CONTEOCONDICIONAL
title  ="Cuantas lineas de conteo condicional?"
msg = "Seleccione el numero de lineas de conteo condicional que quiere poner, se recomiendan maximo 6 pares de lineas de conteo"
choices = ["0","1", "2", "3", "4", "5", "6"]
choice = easygui.choicebox(msg, title, choices)
type(choice)
lineasDeConteoCondicional=int(choice)
print "usted ha seleccionado ",lineasDeConteoCondicional," lineas de conteo condiconal"
contadoresCondicionales=[]
for cc in range(lineasDeConteoCondicional):
    sleep(1)
    lineasDeConteoCondicional=lc.selecttwoLines(imgFile2,ownString='Selecciona la lineas de conteo condiconal' +str(cc+1),filename=archsal,linecount=cc+1)
    contadoresCondicionales.append(lc.conditionalCounter(lineasDeConteoCondicional.pt1,lineasDeConteoCondicional.pt2,lineasDeConteoCondicional.pt3,lineasDeConteoCondicional.pt4,filename=archsal,linecount=cc+1,fps=20))
    sleep(1)
#FINCONTEOCONDICIONAL
#lineaDeConteo=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo',filename=archsal,linecount=1)
#lineaDeConteo2=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo',filename=archsal,linecount=2)
#contar=lc.counter(lineaDeConteo.pt1,lineaDeConteo.pt2,filename=archsal,linecount=1,fps=20) 
#contar2=lc.counter(lineaDeConteo2.pt1,lineaDeConteo2.pt2,filename=archsal,linecount=2,fps=20)    


while True:
    ret_val, imgFile2 = cam.read()
    frames+=1
    if not ret_val:
        print ("Fin del video o salida en camara, saliendo")
        cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
        break
    segframes=cam.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    tiempoactual=cam.get(cv2.cv.CV_CAP_PROP_POS_MSEC)*20.0/30.0
    imgFile3 = cv2.cvtColor(imgFile2,cv2.COLOR_BGR2RGB)
    #imgFile3 = cv2.imread("../data/eagle2.jpg")
    tama=imgFile3.shape
    #imgImported=make_image(tama[1],tama[0],tama[2])
    imgFileptr=copy_iplimage_ptr(imgFile3,imgFileptr,cv_img)
    
    ipl_in2_image(imgFileptr,imgImported)
    #save_image(imgImported,"dog_detect")
    r = detect_img(net, meta, imgImported) 
    if charlador:
        print ('Detecciones: '+str(len(r)))
        print (r)
        
        for i in range(len(r)):
            w=int(r[i][2][2])
            h=int(r[i][2][3])
            x=int(r[i][2][0])-w/2
            y=int(r[i][2][1])-h/2
            #cv2.rectangle(imgFile2, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
    
    for i in range(len(r)):
        if r[i][2][2]<MAXW:
            track.insertNewObject(r[i][2][0],r[i][2][1],r[i][2][2],r[i][2][3],strFeature=r[i][0])
        else:
            print ("        eliminado objeto por tamanio= ",r[i][2][2])
        #w=int(r[i][2][2])
        #h=int(r[i][2][3])
        #x=int(r[i][2][0])-w/2
        #y=int(r[i][2][1])-h/2
            
    if charlador:
        print('Antes de procesar')
        track.printObjets()
        track.printPaths()
        
    track.processObjectstoPaths()

    for j in (range(len(track.p.p[:]))):
        x=int(track.p.p[j].rect.x)
        y=int(track.p.p[j].rect.y)
        u=int(track.p.p[j].rect.u)
        v=int(track.p.p[j].rect.v)
        cv2.rectangle(imgFile2, (x,y), (u,v),track.p.p[j].colour, thickness=4, lineType=8, shift=0)
        if track.p.p[j].contado:
            cv2.putText(imgFile2,str(track.p.p[j].str), (int(track.p.p[j].cp.x),int(track.p.p[j].cp.y)), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255))
        else:
            cv2.putText(imgFile2,str(track.p.p[j].str), (int(track.p.p[j].cp.x),int(track.p.p[j].cp.y)), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255))
    if charlador:
        print('Despues de procesar')
        track.printPaths()

    #Falta graficar los dos ultimos puntos de los paths procesados
    #y si estos pasan la linea de conteo se suma uno

    
    
    for contar in contadores:
        cv2.circle(imgFile2,contar.point1,3,(0,0,255),-1)
        cv2.line(imgFile2,contar.point1,contar.point2,(0,0,255),1)
        cv2.circle(imgFile2,contar.point2,3,(255,0,255),-1)
        
        
    #CONTEOCONDICIONAL
    for contar in contadoresCondicionales:
        cv2.circle(imgFile2,contar.point1,3,(0,0,255),-1)
        cv2.line(imgFile2,contar.point1,contar.point2,(0,0,255),1)
        cv2.circle(imgFile2,contar.point2,3,(255,0,255),-1)
        cv2.circle(imgFile2,contar.point3,3,(255,255,255),-1)
        cv2.line(imgFile2,contar.point3,contar.point4,(255,255,255),1)
        cv2.circle(imgFile2,contar.point4,3,(255,255,255),-1)
    #FINCONTEOCONDICIONAL
        
    # contar los que trayectos que pasen las lineas de conteo
    
    for idx in range(len( track.p.p)):
        if len(track.p.p[idx].path)>2: # si la longitud del path es mayor a dos
            # toma los dos registros mas recientes y los prueba si pasaron la linea de conteo
            p1=(int(track.p.p[idx].path[-1].x),int(track.p.p[idx].path[-1].y))#mas reciente (cuadro actual)
            p2=(int(track.p.p[idx].path[-2].x),int(track.p.p[idx].path[-2].y))#anterior     (cuadro anterior)
            cv2.line(imgFile2,p1,p2,track.p.p[idx].colour,1)

            for contar in contadores:
                if (contar.testLine(p2,p1) and not track.p.p[idx].contadores[contar.linecount]):
                    direct=contar.crossSign(p2,p1)
                    cv2.circle(imgFile2,contar.intersectPoint(p2,p1),4,(100,255,255), -1) #intersecting point
                    track.p.p[idx].contado=True
                    track.p.p[idx].contadores[contar.linecount]=1
                    contar.addToLineCounter(str(track.p.p[idx].str),frames,tiempoactual,direct)
                
            #CONTEOCONDICIONAL    
            for contard in contadoresCondicionales:
                if (contard.testLines(p2,p1) ):#and not (track.p.p[idx].contadoresCondicionales[contard.linecount1] or track.p.p[idx].contadoresCondicionales[contard.linecount2])
                    es1=contard.testLine1(p2,p1)
                    es2=contard.testLine2(p2,p1)
                    if es1:
                        track.p.p[idx].contadoresCondicionales[contard.linecount1]+=1
                        cv2.circle(imgFile2,contard.intersectPoint1(p2,p1),4,(100,100,255), -1) #intersecting point
                        print("Entra 1")
                    if es2:
                        track.p.p[idx].contadoresCondicionales[contard.linecount2]+=1
                        cv2.circle(imgFile2,contard.intersectPoint2(p2,p1),4,(100,255,100), -1) #intersecting point
                        print("Entra 2")
                        
                if track.p.p[idx].contadoresCondicionales[contard.linecount1]>=1 and track.p.p[idx].contadoresCondicionales[contard.linecount2]>=1:
                    if not track.p.p[idx].contadocondicional:
                        track.p.p[idx].contadocondicional=True
                        contard.addToLineCounter(str(track.p.p[idx].str),frames,tiempoactual)
            #CONTEOCONDICIONAL
    
    if pintarTrayectos:
        track.drawPaths(imgFile2)
    
    
    cv2.imshow('Video', imgFile2)
    k = cv2.waitKey(2)& 0xFF
    if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
        print ('interrupcion de usuario...')
        break
    
for contar in contadores:
    contar.saveFinalCounts(frames)
#CONTEOCONDICIONAL 
for contar in contadoresCondicionales:
    contar.saveFinalCounts(frames)
#FINCONTEOCONDICIONAL 
cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
print ('Saliendo...')
cv2.destroyAllWindows()
cam.release()
exit()
