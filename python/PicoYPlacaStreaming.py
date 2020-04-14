#!/usr/bin/python2
# -*- coding: utf-8 -*-
from darknet import *
from Counter import linecounter as lc
from Track import tracking as tr
from time import sleep
import cv2
import os
import easygui
import random
import datetime
import itertools

from  timePicoYPlaca import PicoYPlaca as picoypla



#NUESTRO YOLO ENTRENADO 90000 iteraciones
net = load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta = load_meta("../data/obj.data")

#NUESTRO YOLO ENTRENADO 90000 iteraciones PLACAS
netplacas = load_net("../yolo-PLACAS.cfg", "../../weights/yolo-PLACAS_final.weights", 0)
metaplacas = load_meta("../data/PLACAS.data")

#NUESTRO YOLO ENTRENADO 80000 iteraciones  OCR
netocr = load_net("../yolo-OCR.cfg", "../../weights/yolo-OCR_final.weights", 0)
metaocr = load_meta("../data/OCR.data")


#primera vez
charlador=False
pintarTrayectos=True

SALVARCONTADO=True
contimagen=1


framesttl=10
deCamara=False
MAXW=1920 ## 200 pixeles maximo de ancho permitido
mindist=150

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

def graficarPlacas(img,placa,resOCR,offset=(0,0),imwrite=True):
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
        cv2.imwrite("/home/francisco/test_placas/imagen_capturada_"+cstr+"_"+str(random.randint(10,99))+'.JPG',img)
    
    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
    return (cstr,(x,y-4))
    #if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
    #    print ('interrupcion de usuario...')



folder=easygui.diropenbox(title="Seleccione la carpeta para guardar evidencias",default="/Videos/Streaming")

# TODO revisar existencia de folder en caso de que se seleccione cancelar. 

title  ="Cuantas lineas de deteccion?"
msg = "Seleccione el numero de lineas de deteccion que quiere poner, se recomiendan maximo 2 lineas"
choices = ["1", "2"]
choice = easygui.choicebox(msg, title, choices)
type(choice)
lineasDeConteo=int(choice)
print ("Usted ha seleccionado ",lineasDeConteo," lineas de conteo")

print ("Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo puede que se demore un poco estabilizando el streaming")
from Secretos.secrets import fn,fn1,fn2,fn3
cam = cv2.VideoCapture(fn3)
MAXW=700
mindist=200

for nn in range(100):# se itera un segundo para estabilizar la conexion
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo')
        exit()
    cv2.imshow('Streaming',imgFile2)
    cv2.waitKey(3)
cv2.destroyAllWindows()
cv2.waitKey(2)

imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
#imgFile2 = cv2.imread("../data/eagle.jpg")
tama=imgFile2.shape
imgImported=make_image(tama[1],tama[0],tama[2])

imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
ipl_in2_image(imgFileptr,imgImported)
rgbgr_image(imgImported)

lineaDeConteo=[]
for cc in range(lineasDeConteo):
    lineaDeConteo.append(lc.selectLine(imgFile2,ownString='Selecciona la linea de deteccion #' +str(cc+1),filename=folder+"/deteccion.jpg",linecount=cc+1))
    sleep(1)

pp=picoypla()


while (True):
    
    cam = cv2.VideoCapture(fn)
    ruta,ext=os.path.splitext(fn)
    archsal=folder+'/reporte_streaming.csv'     
    frames=0
    ret_val, imgFile2 = cam.read()
    frames+=1
    if not ret_val:
        print ('ERROR: no se pudo abrir la camara, saliendo')
        exit()
    
    imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
    #imgFile2 = cv2.imread("../data/eagle.jpg")
    tama=imgFile2.shape
    imgImported=make_image(tama[1],tama[0],tama[2])
    
    imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
    ipl_in2_image(imgFileptr,imgImported)
    rgbgr_image(imgImported)
    
    track=tr.tracking(verbose=charlador,mindist=mindist,framesttl=framesttl)#verbose=False,mindist=100
    
    
    contadores=[]
    cc=1
    for linlin in lineaDeConteo:
        contadores.append(lc.counter(linlin.pt1,linlin.pt2,filename=archsal,linecount=cc,fps=20))
        cc+=cc
    ErrorStreaming=False
    while True:
        ret_val, imgFile2 = cam.read()
        frames+=1
        if not ret_val:
            print ("Error en el streaming, saliendo...")
            cv2.imwrite('ultimofotogramaprocesadostreaming.jpg',imgFile3)
            ErrorStreaming=True
            break# TODO PONER REINTENTO
        
        if SALVARCONTADO:
            copiaimagen=imgFile2.copy()
            
        ahora=datetime.datetime.now()
        
        tiempoactual=ahora.strftime("%y-%m-%d-%H%M%S")

        #segframes=cam.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        
        #tiempoactual=cam.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        
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
                if charlador:
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
            cv2.rectangle(imgFile2, (x,y), (u,v),track.p.p[j].colour, thickness=1, lineType=8, shift=0)
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
                        
                        if ((str(track.p.p[idx].str) == 'particular')): #or (str(track.p.p[idx].str) == 'taxi')):
                            try:
                                direct=contar.crossSign(p2,p1)
                                cv2.circle(imgFile2,contar.intersectPoint(p2,p1),4,(100,100,255), -1) #intersecting point
                                cx=int(track.p.p[idx].rect.x)
                                cy=int(track.p.p[idx].rect.y)
                                cu=int(track.p.p[idx].rect.u)
                                cv=int(track.p.p[idx].rect.v)
                                cw=int(track.p.p[idx].tam.w)
                                ch=int(track.p.p[idx].tam.h)
                                
                                imgtoPLACAS=imgFile2[cy:cv,cx:cu]
                                imgtoPLACAS1 = cv2.cvtColor(imgtoPLACAS, cv2.COLOR_BGR2RGB)
                                tamaPL=imgtoPLACAS1.shape
                                imgImportedPL=make_image(tamaPL[1],tamaPL[0],tamaPL[2])
                                
                                imgFileptrPL,cv_img2=get_iplimage_ptr(imgtoPLACAS1)      
                                ipl_in2_image(imgFileptrPL,imgImportedPL)
                                
                                rp = detect_img(netplacas, metaplacas, imgImportedPL) 
                                print ('Detecciones: de placa:'+str(len(rp)))
                                print (rp)
                            except:
                                rp=[]
                                print('Se ha detectado un error en placas particular, toca mirar que es')

                            for i in range(len(rp)):
                                try:
                                    w=int(rp[i][2][2])
                                    h=int(rp[i][2][3])
                                    x=int(rp[i][2][0])-(w/2)
                                    y=int(rp[i][2][1])-(h/2)
                                    placa=[x,y,w,h,rp[i][0]]
                                    imgtoOCR=imgtoPLACAS[y:y+h,x:x+w]
                                    imgtoOCR1 = cv2.cvtColor(imgtoOCR, cv2.COLOR_BGR2RGB)
                                    tama2=imgtoOCR.shape
                                    imgImported2=make_image(tama2[1],tama2[0],tama2[2])
                                    imgFileptr2,cv_img2=get_iplimage_ptr(imgtoOCR1)      
                                    ipl_in2_image(imgFileptr2,imgImported2)
                                    #rgbgr_image(imgImported2)
                                    s = detect_img(netocr, metaocr, imgImported2)
                                    print ('Detecciones: '+str(len(s)))
                                    print (s)
                                    strypos=graficarPlacas(imgFile2,placa,s,offset=(cx,cy))
                                    placa_actual=strypos[0]
                                    
                                    
                                    if pp.tienePicoYPlaca(placa_actual,tipo="particular"):
                                        track.p.p[idx].contado=True
                                        track.p.p[idx].contadores[contar.linecount]=1
                                        contar.addToLineCounter(str(track.p.p[idx].str),frames,tiempoactual,direct)
                                        imfilesave=folder+"/"+placa_actual+'_'+str(contimagen)+'_'+str(random.randint(1000,10000))+'.JPG'
                                        cx=int(track.p.p[idx].rect.x)
                                        cy=int(track.p.p[idx].rect.y)
                                        cu=int(track.p.p[idx].rect.u)
                                        cv=int(track.p.p[idx].rect.v)
                                        cw=int(track.p.p[idx].tam.w)
                                        ch=int(track.p.p[idx].tam.h)
                                        cv2.imwrite(imfilesave,copiaimagen)
                                        contimagen=contimagen+1

                                except TypeError:
                                    print('Se ha detectado un error en OCR particular, toca mirar que es')
                            
                        if ((str(track.p.p[idx].str) == 'taxi')):
                            try:
                                direct=contar.crossSign(p2,p1)
                                cv2.circle(imgFile2,contar.intersectPoint(p2,p1),4,(255,255,255), -1) #intersecting point
                                cx=int(track.p.p[idx].rect.x)
                                cy=int(track.p.p[idx].rect.y)
                                cu=int(track.p.p[idx].rect.u)
                                cv=int(track.p.p[idx].rect.v)
                                cw=int(track.p.p[idx].tam.w)
                                ch=int(track.p.p[idx].tam.h)
                                
                                imgtoPLACAS=imgFile2[cy:cv,cx:cu]
                                imgtoPLACAS1 = cv2.cvtColor(imgtoPLACAS, cv2.COLOR_BGR2RGB)
                                tamaPL=imgtoPLACAS1.shape
                                imgImportedPL=make_image(tamaPL[1],tamaPL[0],tamaPL[2])
                                
                                imgFileptrPL,cv_img2=get_iplimage_ptr(imgtoPLACAS1)      
                                ipl_in2_image(imgFileptrPL,imgImportedPL)
                                
                                rp = detect_img(netplacas, metaplacas, imgImportedPL) 
                                print ('Detecciones: de placa:'+str(len(rp)))
                                print (rp)
                            except:
                                rp=[]
                                print('Se ha detectado un error en placas taxi, toca mirar que es')

                            for i in range(len(rp)):
                                try:
                                    w=int(rp[i][2][2])
                                    h=int(rp[i][2][3])
                                    x=int(rp[i][2][0])-(w/2)
                                    y=int(rp[i][2][1])-(h/2)
                                    placa=[x,y,w,h,rp[i][0]]
                                    imgtoOCR=imgtoPLACAS[y:y+h,x:x+w]
                                    imgtoOCR1 = cv2.cvtColor(imgtoOCR, cv2.COLOR_BGR2RGB)
                                    tama2=imgtoOCR.shape
                                    imgImported2=make_image(tama2[1],tama2[0],tama2[2])
                                    imgFileptr2,cv_img2=get_iplimage_ptr(imgtoOCR1)      
                                    ipl_in2_image(imgFileptr2,imgImported2)
                                    #rgbgr_image(imgImported2)
                                    s = detect_img(netocr, metaocr, imgImported2)
                                    print ('Detecciones: '+str(len(s)))
                                    print (s)
                                    strypos=graficarPlacas(imgFile2,placa,s,offset=(cx,cy))
                                    placa_actual=strypos[0]
                                    
                                    
                                    if pp.tienePicoYPlaca(placa_actual,tipo="taxi"):
                                        track.p.p[idx].contado=True
                                        track.p.p[idx].contadores[contar.linecount]=1
                                        contar.addToLineCounter(str(track.p.p[idx].str),frames,tiempoactual,direct)
                                        imfilesave=folder+"/"+placa_actual+'_'+str(contimagen)+'_'+str(random.randint(1000,10000))+'taxi.JPG'
                                        cx=int(track.p.p[idx].rect.x)
                                        cy=int(track.p.p[idx].rect.y)
                                        cu=int(track.p.p[idx].rect.u)
                                        cv=int(track.p.p[idx].rect.v)
                                        cw=int(track.p.p[idx].tam.w)
                                        ch=int(track.p.p[idx].tam.h)
                                        cv2.imwrite(imfilesave,copiaimagen)
                                        contimagen=contimagen+1

                                except TypeError:
                                    print('Se ha detectado un error en OCR, toca mirar que es')
                    
        if pintarTrayectos:
            track.drawPaths(imgFile2)
        
        
        cv2.imshow('Video', imgFile2)
        k = cv2.waitKey(1)& 0xFF
        if k==ord('q') or k==ord('Q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
            print ('WARNING:::interrupcion de usuario...')
            break
    
    for contar in contadores:
        contar.saveFinalCounts(frames)
    cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
    print ('Saliendo...')
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.waitKey(10)
    cv2.waitKey(100)
    cam.release()
#exit()