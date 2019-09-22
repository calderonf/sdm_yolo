#!/usr/bin/python2
import darknet as dr
from Counter import linecounter as lc
from Track import tracking as tr
from time import sleep
from TimeRounder import round_time_ceil
import cv2
import os
import easygui


import glob
import random
 
"""
#YOLO VOC
net = load_net("../cfg/yolo-voc.cfg", "../../darknet/yolo-voc.weights", 0)
meta = load_meta("../cfg/voc_py.data")
"""
"""
#NUESTRO YOLO ENTRENADO 80000 iteraciones
net = load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta = load_meta("../data/obj.data")
"""

#Yolo entrenado con scooters
net = dr.load_net("../yolo-SCOOTERS.cfg", "../../weights/yolo-SCOOTERS_42000.weights", 0)
meta = dr.load_meta("../data/SCOOTERS.data")

"""
#YOLO COCO
net = load_net("yolo.cfg", "../../darknet/yolo.weights", 0)
meta = load_meta("coco_es.data")
"""
#primera vez
charlador=False
pintarTrayectos=True

SALVARCONTADO=False
contimagen=1


framesttl=5
deCamara=False
MAXW=600 ## 200 pixeles maximo de ancho permitido
mindist=100
 

folder=easygui.diropenbox(title="Seleccione la carpeta destino",default="/VideosSDM/")

title  ="Que Streaming quiere?"
msg = "Seleccione el streaming"
fn1='rtsp://movil:egccol@186.29.90.163:8891/EGC'
fn='rtsp://movil:egccol@186.29.90.163:8891/CamFull2'
fn2='rtsp://multiview:egccol@186.29.90.163:8891/Multiview'
fn3='/home/francisco/videos/Video24Horas_4.mp4'
choices = [fn1,fn,fn2,fn3]
choice = easygui.choicebox(msg, title, choices)
filen=choice
print ("Usted ha seleccionado ",filen," como Video de entrada")
print( "Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo puede que se demore un poco estabilizando el streaming")

cam = cv2.VideoCapture(filen)
cv2.namedWindow( "Streaming",cv2.WINDOW_NORMAL)
for nn in range(100):# se itera unos segundos para estabilizar la conexion 100 cuadros 5 segundos
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo con exit()')
        exit()
    cv2.imshow('Streaming',imgFile2)
    cv2.waitKey(3)
cv2.destroyAllWindows()
cv2.waitKey(2)



title  ="Cuantas lineas de conteo?"
msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
choices = ["1", "2", "3", "4", "5", "6"]
choice = easygui.choicebox(msg, title, choices)
type(choice)
lineasDeConteo=int(choice)
print ("usted ha seleccionado ",lineasDeConteo," lineas de conteo")

print ("Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo")

imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
#imgFile2 = cv2.imread("../data/eagle.jpg")
tama=imgFile2.shape
imgImported=make_image(tama[1],tama[0],tama[2])
imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
ipl_in2_image(imgFileptr,imgImported)
rgbgr_image(imgImported)

lineaDeConteo=[]
for cc in range(lineasDeConteo):
    lineaDeConteo.append(lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo #' +str(cc+1),filename=fn,linecount=cc+1))
    sleep(1)



while(True):
    while (True):
        ret_val, imgFile2 = cam.read()
        if not ret_val:
            print ('Reintento. No abre el video en : ',filen)
            print ("Se espera 1 segundo para reintentar Ctrl+C para salir...")
            sleep(1)
            
    frames=0
    frames+=1
    while(True): 
        #ret_val, imgFile2 = cam.read()
        if not ret_val:
            print ('ERROR: no se pudo abrir la camara, se procede a reintentar...')
            print ("se va a bucle de reintentos")
            break
        
        ahora=datetime.datetime.now()
        nombre_del_archivo=ahora.strftime("CAM00_20%y%m%d%H%M%S_streaming")
        archsal=folder+"/"+nombre_del_archivo+'.csv'     
        
        imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
        #imgFile2 = cv2.imread("../data/eagle.jpg")
        tama=imgFile2.shape
        imgImported=make_image(tama[1],tama[0],tama[2])
        
        imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
        ipl_in2_image(imgFileptr,imgImported)
        rgbgr_image(imgImported)
        track=tr.tracking(verbose=charlador,mindist=mindist,framesttl=framesttl)
        
        contadores=[]
        cc=1
        for linlin in lineaDeConteo:
            contadores.append(lc.counter(linlin.pt1,linlin.pt2,filename=archsal,linecount=cc,fps=20))
            cc+=cc
        print( "Inicia nuevo ciclo de aforo")
        futrq=round_time_ceil()
        while (datetime.datetime.now()<futrq):#Este bucle se rompe cada 15 minutos cada cuarto de hora exacto. 
            ret_val, imgFile2 = cam.read()
            frames+=1
            if not ret_val:
                print ('ERROR: no se pudo abrir la camara, se procede a reintentar por el restante de este cuarto de hora')
                print ("Se espera 1 segundo para reintentar Ctrl+C para salir no se va a guardar el ultimo cuarto por error en video...")
                sleep(1)
                continue
            
            if SALVARCONTADO:
                copiaimagen=imgFile2.copy()
            
            tiempoactual=datetime.datetime.now().strftime("20%y-%m-%d_%H:%M:%S")
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
                            if SALVARCONTADO:
                                imfilesave=folder+"/"+track.p.p[idx].str+'_'+str(contimagen)+'_'+str(random.randint(1000,10000))+'.JPG'
                                cx=int(track.p.p[idx].rect.x)
                                cy=int(track.p.p[idx].rect.y)
                                cu=int(track.p.p[idx].rect.u)
                                cv=int(track.p.p[idx].rect.v)
                                cw=int(track.p.p[idx].tam.w)
                                ch=int(track.p.p[idx].tam.h)
                                cv2.imwrite(imfilesave,copiaimagen[cy:cv,cx:cu])
                                contimagen=contimagen+1
                        
            if pintarTrayectos:
                track.drawPaths(imgFile2)
            
            
            cv2.imshow('Video', imgFile2)
            k = cv2.waitKey(2)& 0xFF
            if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
                print ('Este no sale con q, para salir oprima CTRL+c')
                break
        
        for contar in contadores:
            contar.saveFinalCounts(frames)
    
    cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)


print ('Saliendo Algo raro ya que no deberia pasar por aca...')
cv2.destroyAllWindows()
cam.release()
#exit()
