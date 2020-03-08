#!/usr/bin/python2
from darknet import *
from Counter import linecounter as lc
from Track import tracking as tr
from time import sleep
import cv2
import os
import easygui
import pickle


import glob
import random
 
#primera vez
charlador=False
pintarTrayectos=False

SALVARCONTADO=False
contimagen=1


framesttl=15
deCamara=False
MAXW=1400 ## 200 pixeles maximo de ancho permitido
mindist=150


folder=easygui.diropenbox(title="Seleccione la carpeta con los videos a aforar",default="/media/francisco/monitoreo")

filelist=glob.glob(folder+"/*.avi")
if len(filelist) == 0:
    print("ERROR LA CARPETA NO CONTIENE ARCHIVOS .AVI buscando .mp4")
    filelist=glob.glob(folder+"/*.mp4")
    
filelist.sort()
if len(filelist) == 0:
    print("ERROR LA CARPETA NO CONTIENE ARCHIVOS DE VIDEO SALIENDO")
else:
    if os.path.isfile(folder+"/"+"config.pkl"):
        with open(folder+"/"+"config.pkl") as f:  # Python 3: open(..., 'rb')
            lineasDeConteo, lineasDeConteoCondicional, lineaDeConteo,lineaDeConteoCondicional = pickle.load(f)
        
    else:
        title  ="Cuantas lineas de conteo?"
        msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
        choices = ["0","1", "2", "3", "4", "5", "6"]
        choice = easygui.choicebox(msg, title, choices)
        lineasDeConteo=int(choice)
        print "usted ha seleccionado ",lineasDeConteo," lineas de conteo"
    
        #CONTEOCONDICIONAL
        title  ="Cuantas lineas de conteo condicional?"
        msg = "Seleccione el numero de lineas de conteo condicional que quiere poner, se recomiendan maximo 6 pares de lineas de conteo"
        choices = ["0","1", "2", "3", "4", "5", "6","7"]
        choice2 = easygui.choicebox(msg=msg, title=title, choices=choices)
        lineasDeConteoCondicional=int(choice2)
        print "usted ha seleccionado ",lineasDeConteoCondicional," lineas de conteo condiconal"
        #FINCONTEOCONDICIONAL
        
        
        print "Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo"
        fn=filelist[0]
        cam = cv2.VideoCapture(fn)
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
            sleep(1)
            lineaDeConteo.append(lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo #' +str(cc+1),filename=fn,linecount=cc+1))
            sleep(1)
            
            
        #CONTEOCONDICIONAL
        lineaDeConteoCondicional=[]  
        for cc in range(lineasDeConteoCondicional): 
            sleep(1)
            lineaDeConteoCondicional.append(lc.selecttwoLines(imgFile2,ownString='Selecciona la lineas de conteo condicional' +str(cc+1),filename=fn,linecount=cc+1))
        #FINCONTEOCONDICIONAL
            
        with open(folder+"/"+"config.pkl","w") as f:  # Python 3: open(..., 'rb')
            pickle.dump([lineasDeConteo, lineasDeConteoCondicional, lineaDeConteo,lineaDeConteoCondicional],f)
    
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
        
    print("Aforando ",str(len(filelist)),"Elementos")    
    counterarchivos=1
    for fn in filelist:
        print("procesando archivo ",counterarchivos, " de ",str(len(filelist))) 
        counterarchivos+=1
        #fn = easygui.fileopenbox(default="/media/francisco/SiliconPowerArmor/SDM/",filetypes = ['*.avi','*.mp4'])
        cam = cv2.VideoCapture(fn)
        ruta,ext=os.path.splitext(fn)
        archsal=ruta+'.csv'     
        frames=0
        ret_val, imgFile2 = cam.read()
        frames+=1
        if not ret_val:
            print ('ERROR: no se pudo abrir el archivo de video guardando registro, intentando siguiente')
            with open(folder+"/"+"Error.txt","a") as f:  # Python 3: open(..., 'rb')
                f.write("Error en archivo: "+fn+"\n")
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
            cc+=1
        
        #CONTEOCONDICIONAL
        contadoresCondicionales=[]
        cc=1
        for linlinc in lineaDeConteoCondicional:
            contadoresCondicionales.append(lc.conditionalCounter(linlinc.pt1,linlinc.pt2,linlinc.pt3,linlinc.pt4,filename=archsal,linecount=cc,fps=20))
            cc+=1
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
            
            if SALVARCONTADO:
                copiaimagen=imgFile2.copy()
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
                #else:
                    #print ("        eliminado objeto por tamanio= ",r[i][2][2])
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
                    #CONTEOCONDICIONAL    
                    for contard in contadoresCondicionales:
                        esl2=contard.testLine2(p2,p1)
                        esl1=contard.testLine1(p2,p1)
                        
                        if esl2:
                            track.p.p[idx].contadoresCondicionales[contard.linecount2]+=1
                            cv2.circle(imgFile2,contard.intersectPoint2(p2,p1),4,(100,255,100), -1) #intersecting point
                            
                        if esl1:
                            track.p.p[idx].contadoresCondicionales[contard.linecount1]+=1
                            cv2.circle(imgFile2,contard.intersectPoint1(p2,p1),4,(100,100,255), -1) #intersecting point
                            
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
        for contard in contadoresCondicionales:
            contard.saveFinalCounts(frames)
        #FINCONTEOCONDICIONAL 
        cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
        print ('Saliendo...')
        cv2.destroyAllWindows()
        cv2.waitKey(20)
        cv2.waitKey(2)
        cam.release()
#exit()
