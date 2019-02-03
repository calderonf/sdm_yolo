#!/usr/bin/python2
from darknet import *
import cv2
import easygui

#NUESTRO YOLO ENTRENADO 80000 PLACAS
netplacas = load_net("../yolo-PLACAS.cfg", "../backup_PLACAS/yolo-PLACAS_final.weights", 0)
metaplacas = load_meta("../data/PLACAS.data")

#NUESTRO YOLO ENTRENADO 80000 OCR
netocr = load_net("../yolo-OCR.cfg", "../backup_OCR/yolo-OCR_final.weights", 0)
metaocr = load_meta("../data/OCR.data")

#primera vez
charlador=True

fn = easygui.fileopenbox(default="/home/calderonf/Pictures/",filetypes = ['*.jpg','*.bmp','*.png'])
print (fn)
imgFile2 = cv2.imread(fn)

imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)

tama=imgFile2.shape
imgImported=make_image(tama[1],tama[0],tama[2])

imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
ipl_in2_image(imgFileptr,imgImported)
#rgbgr_image(imgImported)

from testRectangles import rect
        
        
        
        
        
        


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
    cv2.rectangle(imgFile2, (x,y), (u,v),colour, thickness=2, lineType=8, shift=0)
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
        cv2.putText(imgFile2,str(resOCR[j][0]), (xc,vc+10), cv2.FONT_HERSHEY_SIMPLEX,0.6, colour2)
    
    cv2.putText(imgFile2,str(cstr), (x,y-4), cv2.FONT_HERSHEY_SIMPLEX,1, colour)
    cv2.imshow('VideoPLACA', imgFile2)
    k = cv2.waitKey(0)& 0xFF
    cv2.destroyAllWindows()
    #if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
    #    print ('interrupcion de usuario...')



r = detect_img(netplacas, metaplacas, imgImported) 
if charlador:
    print ('Detecciones: '+str(len(r)))
    print (r)
    
for i in range(len(r)):
    w=int(r[i][2][2])
    h=int(r[i][2][3])
    x=int(r[i][2][0])-(w/2)
    y=int(r[i][2][1])-(h/2)
    placa=[x,y,w,h,r[i][0]]
    imgtoOCR=imgFile2[y:y+h,x:x+w]
    imgtoOCR1 = cv2.cvtColor(imgtoOCR, cv2.COLOR_BGR2RGB)
    tama2=imgtoOCR.shape
    imgImported2=make_image(tama2[1],tama2[0],tama2[2])
    imgFileptr2,cv_img2=get_iplimage_ptr(imgtoOCR1)      
    ipl_in2_image(imgFileptr2,imgImported2)
    #rgbgr_image(imgImported2)
    s = detect_img(netocr, metaocr, imgImported2)
    if charlador:
        print ('Detecciones: '+str(len(s)))
        print (s)
    graficarPlacas(imgFile2,placa,s)
        
print ('Saliendo...')
#exit()
























