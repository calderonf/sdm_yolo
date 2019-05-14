#!/usr/bin/python2
from darknet import *
from Counter import linecounter as lc
from Track import tracking as tr
from time import sleep
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

#NUESTRO YOLO ENTRENADO 90000 iteraciones
net = load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta = load_meta("../data/obj.data")

#NUESTRO YOLO ENTRENADO 80000 iteraciones Elem Seguridad ciclistas
netciclistas = load_net("../yolo-OCR.cfg", "../../weights/yolo-ciclistas_final.weights", 0)
metaciclistas = load_meta("../data/OCR.data")

"""
#YOLO COCO
net = load_net("yolo.cfg", "../../darknet/yolo.weights", 0)
meta = load_meta("coco_es.data")
"""
#primera vez
charlador=False
pintarTrayectos=True

SALVARCONTADO=True
contimagen=1


framesttl=5
deCamara=False
MAXW=550 ## 200 pixeles maximo de ancho permitido
mindist=10



def graficarPlacas(img,resplaca,resOCR):
    #tomar las 6 mejores detecciones:
    #resOCR=resOCR[0:6]
    colour=(int(random.uniform(100,150)),int(random.uniform(180,255)),int(0))
    colour2=(int(random.uniform(180,255)),int(random.uniform(100,150)),int(0))
    x=placa[0]
    y=placa[1]
    w=placa[2]
    h=placa[3]
    u=x+w
    v=y+h
    resOCR.sort(key=lambda tup: tup[2][0])#organiza de izquierda a derecha las detecciones del OCR
    #pintar deteccion de placa
    cv2.rectangle(img, (x,y), (u,v),colour, thickness=2, lineType=8, shift=0)
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
        cv2.putText(img,str(resOCR[j][0]), (xc,vc+10), cv2.FONT_HERSHEY_SIMPLEX,0.6, colour2)
    
    cv2.putText(img,str(cstr), (x,y-4), cv2.FONT_HERSHEY_SIMPLEX,1, colour)
    cv2.imshow('VideoPLACA', img)
    k = cv2.waitKey(1)& 0xFF
    #cv2.destroyAllWindows()
    #cv2.waitKey(1)
    return (cstr,(x,y-4))
    #if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
    #    print ('interrupcion de usuario...')



folder=easygui.diropenbox(title="Seleccione la carpeta con los videos a aforar",default="/home/administrador/Videos")

filelist=glob.glob(folder+"/*.avi")
if len(filelist) == 0:
    print("WARNING: LA CARPETA NO CONTIENE ARCHIVOS .avi buscando .mp4 OJO: sensible a mayusculas")
    filelist=glob.glob(folder+"/*.mp4")
    
filelist.sort()
if len(filelist) == 0:
    print("ERROR LA CARPETA NO CONTIENE ARCHIVOS DE VIDEO SALIENDO")
else:
    title  ="Cuantas lineas de conteo?"
    msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
    choices = ["1", "2", "3", "4", "5", "6"]
    choice = easygui.choicebox(msg, title, choices)
    type(choice)
    lineasDeConteo=int(choice)
    print "usted ha seleccionado ",lineasDeConteo," lineas de conteo"
    
    print "Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo"
    fn=filelist[0]
    cam = cv2.VideoCapture(fn)
    MAXW=700
    mindist=200  
    ret_val, imgFile2 = cam.read()
    if not ret_val:
        print ('ERROR:  no se pudo abrir la camara, saliendo')
        exit()
    
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
    
    for fn in filelist:
        
        cam = cv2.VideoCapture(fn)
        ruta,ext=os.path.splitext(fn)
        archsal=ruta+'.csv'     
        frames=0
        ret_val, imgFile2 = cam.read()
        frames+=1
        if not ret_val:
            print ('ERROR: no se pudo abrir el video, saliendo')
            exit()
        
        imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
        
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
        
        
        #lineaDeConteo=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo',filename=archsal,linecount=1)
        #lineaDeConteo2=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo',filename=archsal,linecount=2)
        #contar=lc.counter(lineaDeConteo.pt1,lineaDeConteo.pt2,filename=archsal,linecount=1,fps=20) 
        #contar2=lc.counter(lineaDeConteo2.pt1,lineaDeConteo2.pt2,filename=archsal,linecount=2,fps=20)    
        
        
        
        
        while True:
            ret_val, imgFile2 = cam.read()
            frames+=1
            if not ret_val:
                print ("Fin del video o salida en camara, saliendo")
                #cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
                break
            
            if SALVARCONTADO:
                copiaimagen=imgFile2.copy()
            segframes=cam.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            tiempoactual=cam.get(cv2.cv.CV_CAP_PROP_POS_MSEC)*20.0/30.0#el 20.0/30.0 es por defecto en videos de secretaria. 
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
                            if ((str(track.p.p[idx].str) == 'ciclista'):
                                rp = detect_img(netplacas, metaplacas, imgImported) 

                                print ('Detecciones: de placa:'+str(len(rp)))
                                print (rp)

                                for i in range(len(rp)):
                                    w=int(rp[i][2][2])
                                    h=int(rp[i][2][3])
                                    x=int(rp[i][2][0])-(w/2)
                                    y=int(rp[i][2][1])-(h/2)
                                    placa=[x,y,w,h,rp[i][0]]
                                    imgtoOCR=imgFile2[y:y+h,x:x+w]
                                    imgtoOCR1 = cv2.cvtColor(imgtoOCR, cv2.COLOR_BGR2RGB)
                                    tama2=imgtoOCR.shape
                                    imgImported2=make_image(tama2[1],tama2[0],tama2[2])
                                    imgFileptr2,cv_img2=get_iplimage_ptr(imgtoOCR1)      
                                    ipl_in2_image(imgFileptr2,imgImported2)
                                    #rgbgr_image(imgImported2)
                                    s = detect_img(netocr, metaocr, imgImported2)
                                    print ('Detecciones: '+str(len(s)))
                                    print (s)
                                    graficarPlacas(imgFile2,placa,s)
                                    
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
                print ('interrupcion de usuario...')
                break
        
        for contar in contadores:
            contar.saveFinalCounts(frames)
        cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
        print ('Saliendo...')
        cv2.destroyAllWindows()
        cam.release()
#exit()
