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

from  timePicoYPlaca import PicoYPlaca as picoypla

from grabarVideo import grabadorVideos



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


framesttl=20*2
MAXW=1920/2 ## 200 pixeles maximo de ancho permitido
mindist=150
placa_actual=""

FPS=20
SegundosCebra=6
MAXCONTEOCEBRA=FPS*SegundosCebra


TEXTOPICOYPLACA="C14"
TEXTOCEBRA="C31"
AMPLIADA="A"
PANORAMICA="P"


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



folder=easygui.diropenbox(title="Seleccione la carpeta para guardar evidencias",default="/VideosSDM")


if not os.path.exists(folder+"/"+TEXTOPICOYPLACA):
    os.mkdir(folder+"/"+TEXTOPICOYPLACA)

if not os.path.exists(folder+"/"+TEXTOCEBRA):
    os.mkdir(folder+"/"+TEXTOCEBRA)


# TODO revisar existencia de folder en caso de que se seleccione cancelar. 

title  ="Cuantas lineas de deteccion?"
msg = "Seleccione el numero de lineas de deteccion que quiere poner, se recomiendan maximo 2 lineas"
choices = ["1", "2"]
choice = easygui.choicebox(msg, title, choices)
lineasDeConteo=int(choice)
print "Usted ha seleccionado ",lineasDeConteo," lineas de conteo"

regionesZebra=1

title  ="Cuantas regiones de deteccion?"
msg = "Seleccione el numero de regiones de deteccion que quiere poner, se recomiendan maximo 1 regiones"
choices = ["1"]
choice = easygui.choicebox(msg, title, choices)
regionesZebra=int(choice)
print "Usted ha seleccionado ",regionesZebra," regiones de ceteccion de Cebra"


title  ="Que Streaming o video quiere?"
msg = "Seleccione el streaming"
from Secretos.secrets import fn,fn1,fn2,fn3
choices = [fn,fn1,fn2,fn3]
choice = easygui.choicebox(msg, title, choices)
filen=choice
print "Usted ha seleccionado ",filen," como Video de entrada"

title  ="Que Direccion de Camara esta usando?"
msg = "Seleccione el direccion"
fn='CR7-CL45'
fn1='CR19-CL100'
fn2='PONGAQUIDIRECCION'
choices = [fn,fn1,fn2,fn3]
choice = easygui.choicebox(msg, title, choices)
TEXTODIRECCION=choice
print "Usted ha seleccionado ",TEXTODIRECCION," como Video de entrada"


title  ="Que Dlocalidad tiene la camara que esta usando?"
msg = "Seleccione localidad"
fn='CHAPINERO'
fn1='USAQUEN'
fn2='PONGAQUILOCALIDAD'
choices = [fn,fn1,fn2,fn3]
choice = easygui.choicebox(msg, title, choices)
TEXTOLOCALIDAD=choice
print "Usted ha seleccionado ",TEXTOLOCALIDAD," como Video de entrada"

print "Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo puede que se demore un poco estabilizando el streaming"

cam = cv2.VideoCapture(filen)

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


regionCebra=[]
for rc in range(regionesZebra):
    regionCebra.append(lc.selectRect(imgFile2,ownString='Selecciona la region de deteccion #' +str(cc+1),filename=folder+"/deteccion.jpg",linecount=cc+1))
    sleep(1)

pp=picoypla()
grabar=grabadorVideos()

print ("Listos todos los valores de inicializacion cargando programa...")

while (True):
    
    cam = cv2.VideoCapture(filen)
    
    archsal=folder+'/reporte_streaming.csv'     
    frames=0
    ret_val, imgFile2 = cam.read()
    frames+=1
    if not ret_val:
        print ('ERROR: no se pudo abrir la camara, reintentando')
        sleep(5)
        continue
        #exit()
    
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

    regiones=[]
    cc=1
    for linlin in regionCebra:
        regiones.append(lc.zone_detector(linlin.pt1,linlin.pt2,linlin.pt3,linlin.pt4,imgFile2))
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
        
        grabar.procesarCuadro(copiaimagen)
        
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
            if track.p.p[j].detectadoCebra:
                cv2.putText(imgFile2,str(track.p.p[j].contadorCebra), (int(x),int(y+20)), cv2.FONT_HERSHEY_SIMPLEX,1, (255,120,140))
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
            if len(track.p.p[idx].path)>=2: # si la longitud del path es mayor o igual a dos
                #buscar si el path esta dentro de la region de cebra
                for cebra in regiones:
                    if cebra.listPointsInside(track.p.p[idx].puntosFrontera) and cebra.esComparendiable(track.p.p[idx].str):
                        track.p.p[idx].contadorCebra+=1#acumular uno al conteo del path
            
                #si lleva mas de MAXCONTEOCEBRA cuadros acmulados
            
                if track.p.p[idx].contadorCebra>=MAXCONTEOCEBRA and (not track.p.p[idx].detectadoCebra):
                    try:
                        placa_actual="PLACA_NO_DETECTADA"
                        track.p.p[idx].detectadoCebra=True
                        print ("*"*30)
                        print (" "*10+"Infraccion detectada"+" "*10)
                        print ("*"*30)
                        
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
                        
                        for i in range(len(rp)):
                            placa_actual="PLACA"+str(track.p.p[idx].idx)
                            
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
                            except:
                                print("Error en placa interno") 
                        
                    except:
                        print("Error en placa busqueda en imagen interna detectado. ")
                    
                    print ("*"*30)
                    print (" "*13+"PLACA"+" "*13)
                    print (" "*10+placa_actual+" "*10)
                    print ("*"*30)
                    ahora=datetime.datetime.now()
                    fechaformatotexto=ahora.strftime("%d-%m-20%y %H_%M_%S")
                    #imfilesave=folder+"/"+TEXTOCEBRA+"/"+placa_actual+'-'+TEXTOCEBRA+'-'+AMPLIADA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+'.JPG'
                    #cv2.imwrite(imfilesave,copiaimagen)
                    imfilesave=folder+"/"+TEXTOCEBRA+"/"+placa_actual+'-'+TEXTOCEBRA+'-'+PANORAMICA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+'.JPG'
                    cv2.imwrite(imfilesave,copiaimagen)
                    imfilesavev=folder+"/"+TEXTOCEBRA+"/"+placa_actual+'-'+TEXTOCEBRA+'-'+"V"+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+'.avi'
                    imfilesavef2=folder+"/"+TEXTOCEBRA+"/"+placa_actual+'-'+TEXTOCEBRA+'-'+AMPLIADA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+'.JPG'
                    grabar.nuevoVideo(imfilesavev,imfilesavef2)
                    
                    
                
                
                # toma los dos registros mas recientes y los prueba si pasaron la linea de conteo para encontrar pico y placa
                p1=(int(track.p.p[idx].path[-1].x),int(track.p.p[idx].path[-1].y))#mas reciente (cuadro actual)
                p2=(int(track.p.p[idx].path[-2].x),int(track.p.p[idx].path[-2].y))#anterior     (cuadro anterior)
                cv2.line(imgFile2,p1,p2,track.p.p[idx].colour,1)
                for contar in contadores:
                    if (contar.testLine(p2,p1) and not track.p.p[idx].contadores[contar.linecount]):# si pasa la linea de conteo.
                        
                        if (str(track.p.p[idx].str) == 'particular'): #or (str(track.p.p[idx].str) == 'taxi')):
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
                                        cx=int(track.p.p[idx].rect.x)
                                        cy=int(track.p.p[idx].rect.y)
                                        cu=int(track.p.p[idx].rect.u)
                                        cv=int(track.p.p[idx].rect.v)
                                        cw=int(track.p.p[idx].tam.w)
                                        ch=int(track.p.p[idx].tam.h)
                                        
                                        ahora=datetime.datetime.now()
                                        fechaformatotexto=ahora.strftime("%d-%m-20%y %H_%M_%S")
                                        imfilesave=folder+"/"+TEXTOPICOYPLACA+"/"+placa_actual+'-'+TEXTOPICOYPLACA+'-'+AMPLIADA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+' revParticular.JPG'
                                        cv2.imwrite(imfilesave,copiaimagen)
                                        imfilesave=folder+"/"+TEXTOPICOYPLACA+"/"+placa_actual+'-'+TEXTOPICOYPLACA+'-'+PANORAMICA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+' revParticular.JPG'
                                        cv2.imwrite(imfilesave,copiaimagen)
                                        #imfilesave=folder+"/"+TEXTOPICOYPLACA+"/"+placa_actual+'-'+TEXTOPICOYPLACA+'-'+"V"+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+' revParticular.avi'
                                        #grabar.nuevoVideo(imfilesave,TTL=20)
                                        
                                        contimagen=contimagen+1

                                except TypeError:
                                    print('Se ha detectado un error en OCR particular, toca mirar que es')
                            
                        if (str(track.p.p[idx].str) == 'taxi'):
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
                                        cx=int(track.p.p[idx].rect.x)
                                        cy=int(track.p.p[idx].rect.y)
                                        cu=int(track.p.p[idx].rect.u)
                                        cv=int(track.p.p[idx].rect.v)
                                        cw=int(track.p.p[idx].tam.w)
                                        ch=int(track.p.p[idx].tam.h)
                                        ahora=datetime.datetime.now()
                                        fechaformatotexto=ahora.strftime("%d-%m-20%y %H_%M_%S")
                                        imfilesave=folder+"/"+TEXTOPICOYPLACA+"/"+placa_actual+'-'+TEXTOPICOYPLACA+'-'+AMPLIADA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+' revPublico.JPG'
                                        cv2.imwrite(imfilesave,copiaimagen)
                                        imfilesave=folder+"/"+TEXTOPICOYPLACA+"/"+placa_actual+'-'+TEXTOPICOYPLACA+'-'+PANORAMICA+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+' revPublico.JPG'
                                        cv2.imwrite(imfilesave,copiaimagen)
                                        #imfilesave=folder+"/"+TEXTOPICOYPLACA+"/"+placa_actual+'-'+TEXTOPICOYPLACA+'-'+"V"+'-'+TEXTODIRECCION+'-'+TEXTOLOCALIDAD+'-'+fechaformatotexto+' revPublico.avi'
                                        #grabar.nuevoVideo(imfilesave,TTL=20)
                                        
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