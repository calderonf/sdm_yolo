 # en base a https://stackoverflow.com/questions/29791075/counting-the-point-which-intercept-in-a-line-with-opencv-python 
import cv2
import numpy as np
import collections
import os


CLASSES="version_2"

"""
events = [i for i in dir(cv2) if 'EVENT' in i]
print events
['EVENT_FLAG_ALTKEY', 'EVENT_FLAG_CTRLKEY', 'EVENT_FLAG_LBUTTON', 'EVENT_FLAG_MBUTTON', 'EVENT_FLAG_RBUTTON',
 'EVENT_FLAG_SHIFTKEY', 'EVENT_LBUTTONDBLCLK', 'EVENT_LBUTTONDOWN', 'EVENT_LBUTTONUP', 'EVENT_MBUTTONDBLCLK',
 'EVENT_MBUTTONDOWN', 'EVENT_MBUTTONUP', 'EVENT_MOUSEMOVE', 'EVENT_RBUTTONDBLCLK', 'EVENT_RBUTTONDOWN', 'EVENT_RBUTTONUP']
"""

drawing = False # true if mouse is pressed
both = False
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
iix,iiy = -1,-1
ox,oy=-1,-1
# Clases Version 1 
#num2clases=['peaton', 'particular', 'taxi', 'motociclista', 'bus', 'camion', 'minivan', 'ciclista', 'tractomula']
# Clases Version 2
#num2clases=['peaton', 'particular', 'taxi', 'motociclista', 'bus', 'camion', 'minivan', 'ciclista', 'tractomula', 'scooter', 'bicitaxi']
# Clases Version UMV 
#num2clases=['Camion_C1', 'Camion_C2', 'Camion_C3', 'Camion_C4', 'Camion_C5', 'Camion_C6', 'Auto', 'Colectivo', 'Bus']
#clases={'Camion_C1': 0, 'Camion_C2': 1, 'Camion_C3': 2, 'Camion_C4': 3, 'Camion_C5': 4, 'Camion_C6': 5, 'Auto': 6, 'Colectivo': 7, 'Bus': 8}


if CLASSES=="version_1":
    # Clases Version 1
    num2clases=['peaton', 'particular', 'taxi', 'motociclista', 'bus', 'camion', 'minivan', 'ciclista', 'tractomula']
    clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}

elif CLASSES=="version_2":
    # Clases Version 2
    num2clases=['peaton', 'particular', 'taxi', 'motociclista', 'bus', 'camion', 'minivan', 'ciclista', 'tractomula', 'scooter', 'bicitaxi']
    clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8, 'scooter':9, 'bicitaxi':10}

elif CLASSES=="Version_UMV":
    # Clases Version UMV 
    num2clases=['Camion_C1', 'Camion_C2', 'Camion_C3', 'Camion_C4', 'Camion_C5', 'Camion_C6', 'Auto', 'Colectivo', 'Bus']
    clases={'Camion_C1': 0, 'Camion_C2': 1, 'Camion_C3': 2, 'Camion_C4': 3, 'Camion_C5': 4, 'Camion_C6': 5, 'Auto': 6, 'Colectivo': 7, 'Bus': 8}



def callbackMouse(event,x,y,flags,param):
    global ix,iy,iix,iiy,ox,oy,drawing,both

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            ox,oy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        iix,iiy = x,y
        drawing = False
        both = True
        
class selecttwoLines:
    def __init__(self,imag,ownString='Seleccione un par de puntos para crear una linea ',filename='Linea_de_conteo.jpg',linecount=1):
        global ix,iy,uux,iiy,ox,oy,drawing,both
        self.pt1=(-1,-1)
        self.pt2=(-1,-1)
        self.pt3=(-1,-1)
        self.pt4=(-1,-1)
        self.error=True
        print ("Por favor sobre la ventana:")
        print(ownString+" 1 de 2")
        print ("la primera linea de conteo condicional")
        print (20*"_")
        print ("Instrucciones:")
        print ("1. seleccione un punto de inicio con el click derecho")
        print ("2. mantenga sostenido el click y suelte donde quiera el otro punto")
        print ("3. oprima q, Q, s, S o Esc para salir en cualquier momento y retornar la no seleccion de puntos")
        
        cv2.namedWindow('Seleccione Linea 1 de 2')
        cv2.setMouseCallback('Seleccione Linea 1 de 2',callbackMouse)
        
        while(1):
            img=imag.copy()
            if drawing:
                cv2.circle(img,(ix,iy),3,(0,0,255),-1)
                cv2.line(img,(ix,iy),(ox,oy),(255,122,110),2)
                cv2.circle(img,(ox,oy),3,(255,0,255),-1)
            cv2.imshow('Seleccione Linea 1 de 2',img)
            k = cv2.waitKey(1) & 0xFF
            if both:
                self.pt1=(ix,iy)
                self.pt2=(iix,iiy)
                self.error=False
                break
                
            if k == 27 or k==ord('q') or k==ord('Q') or k==ord('s') or k==ord('S'):
                self.pt1=(-1,-1)
                self.pt2=(-1,-1)
                self.error=True
                break
        #filenameraw, file_extension = os.path.splitext(filename)
        #self.archivosalidajpg=filenameraw+'_linea_'+str(linecount)+'.jpg'
        #cv2.imwrite(self.archivosalidajpg,img)
        ix,iy=-1,-1
        uux,iiy=-1,-1
        ox,oy=-1,-1
        drawing,both=False,False
        print ("puntos 1 de 2 listos, gracias",self.pt1,self.pt2)
        cv2.destroyWindow('Seleccione Linea 1 de 2')
        k = cv2.waitKey(1)
        
        print ("Por favor sobre la ventana:")
        print(ownString+" 2 de 2")
        print ("la segunda linea de conteo condicional")
        print (20*"_")
        print ("Instrucciones:")
        print ("1. seleccione un punto de inicio con el click derecho")
        print ("2. mantenga sostenido el click y suelte donde quiera el otro punto")
        print ("3. oprima q, Q, s, S o Esc para salir en cualquier momento y retornar la no seleccion de puntos")
        
        cv2.namedWindow('Seleccione Linea 2 de 2')
        cv2.setMouseCallback('Seleccione Linea 2 de 2',callbackMouse)
        
        while(1):
            img=imag.copy()
            if drawing:
                cv2.circle(img,(ix,iy),3,(0,0,255),-1)
                cv2.line(img,(ix,iy),(ox,oy),(255,122,110),2)
                cv2.circle(img,(ox,oy),3,(255,0,255),-1)
            cv2.imshow('Seleccione Linea 2 de 2',img)
            k = cv2.waitKey(1) & 0xFF
            if both:
                self.pt3=(ix,iy)
                self.pt4=(iix,iiy)
                self.error=False
                break
                
            if k == 27 or k==ord('q') or k==ord('Q') or k==ord('s') or k==ord('S'):
                self.pt1=(-1,-1)
                self.pt2=(-1,-1)
                self.pt3=(-1,-1)
                self.pt4=(-1,-1)
                self.error=True
                break
        filenameraw, file_extension = os.path.splitext(filename)
        self.archivosalidajpg=filenameraw+'_lineaCondicional_'+str(linecount)+'.jpg'
        
        cv2.circle(img,self.pt1,3,(50,50,255),-1)
        cv2.line(img,self.pt1,self.pt2,(255,122,200),2)
        cv2.circle(img,self.pt2,3,(255,50,255),-1)

        cv2.imwrite(self.archivosalidajpg,img)
        ix,iy=-1,-1
        uux,iiy=-1,-1
        ox,oy=-1,-1
        drawing,both=False,False
        print ("puntos 2 de 2 listos, gracias",self.pt1,self.pt2)
        cv2.destroyWindow('Seleccione Linea 2 de 2')
        k = cv2.waitKey(1)
        
        
class selectLine:
    
    def __init__(self,imag,ownString='Seleccione un par de puntos para crear una linea ',filename='Linea_de_conteo.jpg',linecount=1,DefaultPoints=False,pt1=(-1,-1),pt2=(-1,-1)):

        if DefaultPoints:
            global ix,iy,uux,iiy,ox,oy,drawing,both
            img=imag.copy()
            
            cv2.circle(img,pt1,3,(0,0,255),-1)
            cv2.line(img,pt1,pt2,(255,122,110),2)
            cv2.circle(img,pt2,3,(255,0,255),-1)
            
            cv2.imshow('Seleccion de Puntos',img)
            k = cv2.waitKey(2000) & 0xFF
            self.pt1=pt1
            self.pt2=pt2
            self.error=False
            #TODO comprobar que los puntos sean menores al tamanio de la imagen
            filenameraw, file_extension = os.path.splitext(filename)
            self.archivosalidajpg=filenameraw+'_linea_'+str(linecount)+'.jpg'
            print ("puntos listos, configurados por defecto en: ",self.pt1,self.pt2)
            cv2.destroyWindow('Seleccion de Puntos')
        else:
            global ix,iy,uux,iiy,ox,oy,drawing,both
            self.pt1=(-1,-1)
            self.pt2=(-1,-1)
            self.error=True
            
            print ("Por favor sobre la ventana llamada:")
            print ("Seleccione Puntos")
            print(ownString)
            print (20*"_")
            print ("Instrucciones:")
            print ("1. seleccione un punto de inicio con el click derecho")
            print ("2. mantenga sostenido el click y suelte donde quiera el otro punto")
            print ("3. oprima q, Q, s, S o Esc para salir en cualquier momento y retornar la no seleccion de puntos")
            
            cv2.namedWindow('Seleccione Puntos')
            cv2.setMouseCallback('Seleccione Puntos',callbackMouse)
            
            while(1):
                img=imag.copy()
                if drawing:
                    cv2.circle(img,(ix,iy),3,(0,0,255),-1)
                    cv2.line(img,(ix,iy),(ox,oy),(255,122,110),2)
                    cv2.circle(img,(ox,oy),3,(255,0,255),-1)
                cv2.imshow('Seleccione Puntos',img)
                k = cv2.waitKey(1) & 0xFF
                if both:
                    self.pt1=(ix,iy)
                    self.pt2=(iix,iiy)
                    self.error=False
                    break
                    
                if k == 27 or k==ord('q') or k==ord('Q') or k==ord('s') or k==ord('S'):
                    self.pt1=(-1,-1)
                    self.pt2=(-1,-1)
                    self.error=True
                    break
            filenameraw, file_extension = os.path.splitext(filename)
            self.archivosalidajpg=filenameraw+'_linea_'+str(linecount)+'.jpg'
            cv2.imwrite(self.archivosalidajpg,img)
            ix,iy=-1,-1
            uux,iiy=-1,-1
            ox,oy=-1,-1
            drawing,both=False,False
            print ("puntos listos, gracias",self.pt1,self.pt2)
            k = cv2.waitKey(1)
            cv2.destroyWindow('Seleccione Puntos')
            k = cv2.waitKey(1)

class selectRect:
    
    def __init__(self,imag,ownString='Seleccione Dos lineas que limitan la region a supervisar ',filename='Region.jpg',linecount=1,DefaultPoints=False,pt1=(-1,-1),pt2=(-1,-1),pt3=(-1,-1),pt4=(-1,-1)):
        
        if DefaultPoints:
            global ix,iy,uux,iiy,ox,oy,drawing,both
            
            img=imag.copy()
            self.pt1=pt1
            self.pt2=pt2
            self.pt3=pt3
            self.pt4=pt4
            polygon=[self.pt1,self.pt2,self.pt4,self.pt3]
            self.error=False
            
            tambase=img.shape
            mask = np.zeros((tambase[0],tambase[1],1), np.uint8)
            maskrgb = np.zeros(tambase, np.uint8)
            
            pts = np.array(polygon, np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.fillConvexPoly(mask,pts,(255))
            cv2.fillConvexPoly(maskrgb,pts,(255,255,255))
            alpha =0.5
            cv2.addWeighted(maskrgb, alpha, img, 1,0, img)        
            
            filenameraw, file_extension = os.path.splitext(filename)
            self.archivosalidajpg=filenameraw+'Rect'+str(linecount)+'.jpg'
            
            cv2.imwrite(self.archivosalidajpg,img)
            print ("Ultimos 2 puntos listos, gracias",self.pt3,self.pt4)
            cv2.imshow('Seleccion de Puntos',img)
            k = cv2.waitKey(2000) & 0xFF
            print ("puntos listos, configurados por defecto en: ",self.pt1,self.pt2)
            print ("y en                                        ",self.pt3,self.pt4)
            cv2.destroyWindow('Seleccion de Puntos')
            
        else:
        
            global ix,iy,uux,iiy,ox,oy,drawing,both
            
            self.pt1=(-1,-1)
            self.pt2=(-1,-1)
            self.pt3=(-1,-1)
            self.pt4=(-1,-1)
            
            filenameraw, file_extension = os.path.splitext(filename)
            self.archivosalidajpg=filenameraw+'Rect'+str(linecount)+'.jpg'
            
            self.error=True
            print ("Por favor sobre la ventana llamada:")
            print ("Seleccione Rectangulo")
            print(ownString)
            print (20*"_")
            print ("Instrucciones:")
            print ("1. seleccione un punto de inicio con el click derecho")
            print ("2. mantenga sostenido el click y suelte donde quiera el otro punto")
            print ("3. oprima q, Q, s, S o Esc para salir en cualquier momento y retornar la no seleccion de puntos")
            
            cv2.namedWindow('Seleccione Rectangulo 1')
            cv2.setMouseCallback('Seleccione Rectangulo 1',callbackMouse)
            
            while(1):
                img=imag.copy()
                if drawing:
                    cv2.circle(img,(ix,iy),3,(0,0,255),-1)
                    cv2.line(img,(ix,iy),(ox,oy),(255,122,110),2)
                    cv2.circle(img,(ox,oy),3,(255,0,255),-1)
                cv2.imshow('Seleccione Rectangulo 1',img)
                k = cv2.waitKey(1) & 0xFF
                if both:
                    self.pt1=(ix,iy)
                    self.pt2=(iix,iiy)
                    self.error=False
                    break
                    
                if k == 27 or k==ord('q') or k==ord('Q') or k==ord('s') or k==ord('S'):
                    self.pt1=(-1,-1)
                    self.pt2=(-1,-1)
                    self.error=True
                    break
            #filenameraw, file_extension = os.path.splitext(filename)
            #self.archivosalidajpg=filenameraw+'_Region_'+str(linecount)+'.jpg'
            #cv2.imwrite(self.archivosalidajpg,img)
            ix,iy=-1,-1
            uux,iiy=-1,-1
            ox,oy=-1,-1
            drawing,both=False,False
            print ("Primeros 2 puntos listos, gracias continuando con 3 y 4",self.pt1,self.pt2)
            cv2.destroyWindow('Seleccione Rectangulo 1')
            
            cv2.namedWindow('Seleccione Rectangulo 2')
            cv2.setMouseCallback('Seleccione Rectangulo 2',callbackMouse)
            
            while(1):
                img=imag.copy()
                cv2.circle(img,self.pt1,3,(0,0,255),-1)
                cv2.line(img,self.pt1,self.pt2,(110,122,255),2)
                cv2.circle(img,self.pt2,3,(255,0,255),-1)
                if drawing:
                    cv2.circle(img,(ix,iy),3,(0,0,255),-1)
                    cv2.line(img,(ix,iy),(ox,oy),(255,122,110),2)
                    cv2.circle(img,(ox,oy),3,(255,0,255),-1)
                cv2.imshow('Seleccione Rectangulo 2',img)
                k = cv2.waitKey(1) & 0xFF
                if both:
                    self.pt3=(ix,iy)
                    self.pt4=(iix,iiy)
                    self.error=False
                    break
                if k == 27 or k==ord('q') or k==ord('Q') or k==ord('s') or k==ord('S'):
                    self.pt3=(-1,-1)
                    self.pt4=(-1,-1)
                    self.error=True
                    break
            filenameraw, file_extension = os.path.splitext(filename)
            self.archivosalidajpg=filenameraw+'Rect'+str(linecount)+'.jpg'
            
    
            polygon=[self.pt1,self.pt2,self.pt4,self.pt3]
            
            tambase=img.shape
            mask = np.zeros((tambase[0],tambase[1],1), np.uint8)
            maskrgb = np.zeros(tambase, np.uint8)
            
            pts = np.array(polygon, np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.fillConvexPoly(mask,pts,(255))
            cv2.fillConvexPoly(maskrgb,pts,(255,255,255))
            
            alpha =0.5
            cv2.addWeighted(maskrgb, alpha, img, 1,0, img)        
            
            cv2.imwrite(self.archivosalidajpg,img)
            ix,iy=-1,-1
            uux,iiy=-1,-1
            ox,oy=-1,-1
            drawing,both=False,False
            print ("Ultimos 2 puntos listos, gracias",self.pt3,self.pt4)
            cv2.destroyWindow('Seleccione Rectangulo 2')
        
        
        
        
    def printRect(self):
        print ("Los 4 Puntos del rectangulo son:",self.pt1,self.pt2,self.pt3,self.pt4)
        
        

class saveAndLoadParser:
    def __init__(self, filename="salida.txt"):
        self.filename=filename
        print ("guardando archivo en "+filename )
        
    def resetFile(self):
        self.FILE = open(self.filename,'w')
        self.FILE.close()
        
    def appendFile(self,writestring):
        self.FILE = open(self.filename,'a')
        self.FILE.write(str(writestring))
        self.FILE.close()

    def openFileToRead(self):
        self.FILE = open(self.filename,'r')
        
    def readLine(self):
        return self.FILE.readline()
        
    def writeData(self,nameofdata,data):
        
        nameofdata=nameofdata.rstrip()
        if type(data) is list:
            self.appendFile("list="+nameofdata+"="+str(data)+"\n")
        elif type(data) is str:
            self.appendFile("string="+nameofdata+"="+str(data.rstrip())+"\n")
        elif type(data) is float:
            self.appendFile("float="+nameofdata+"="+str(data)+"\n")
        elif type(data) is int:
            self.appendFile("int="+nameofdata+"="+str(data)+"\n")
        else:
            print ("ERROR: tipo "+str(type(data))+" No soportado")
            return 1
        return 0
            
    def closeFile(self):
        self.FILE.close()


    def readData(self):
        mystr=self.readLine()
        if mystr=='':
            return 0,0,0
        if mystr=='\n':
            return -1,-1,-1
        mystr=mystr.rstrip()
        ln=mystr.split('=')
        tipo=ln[0]
        nombre=ln[1]
        
        if tipo == 'list':
            datos=eval(ln[2])
        elif tipo ==  'string':
            datos=ln[2].rstrip()
        elif tipo == 'float':
            datos=eval(ln[2])
        elif tipo == 'int':
            datos=eval(ln[2])
        else:
            print ("ERROR: tipo "+tipo+" No soportado")
            return 1,1,1        
        return tipo,nombre,datos


class zone_detector:
    
    def __init__(self, pt1,pt2,pt3,pt4,imagebase,filename="salidaZoneDetector.csv",fps=20,linecount=1):
        """
        Inicializacion\n
        Clase counter \n
        Esta clase lista todos los Metodos para generar la clase de deteccion de objeto por zona \n
        Ella genera al inicio los llamados a las clases internas objects y paths,\n
        \n
        La clase objects sirve para llevar registro de los objetos detectados en el cuadro actual\n
        La clase paths sirve para llevar registro del trajecto asociado a cada objeto detectado\n
    
        los metodos son: \n
            __init__ \n
            calcOwnParams \n
            calcParams \n
            testLine \n
            intersectPoint \n
            addToLineCounter \n
            writeToLineCounter \n
            
            SaveLine \n
            LoadLine \n
            
            printPaths \n
            clearObjets \n
            clearPaths \n
            processObjectstoPaths \n
            
            __areLinesIntersecting
            __returnIntersectPoint
            
        \n
        USO:\n
        \n
        pedir puntos de conteo\n
        procesar si trajecto pasa linea de conteo\n
        profit\n
        LLAMADO:\n
            \n
        EJEMPLOS:\n
         
        """
        self.Params = collections.namedtuple('Params', ['a','b','c']) #para guardar la ecuacion de una linea
        
        self.point1 = pt1
        self.point2 = pt2
        self.point3 = pt3
        self.point4 = pt4
        self.polygon=[pt1,pt2,pt4,pt3]
        
        
        
        self.tambase=imagebase.shape
        self.mask = np.zeros((self.tambase[0],self.tambase[1],1), np.uint8)
        self.maskrgb = np.zeros(self.tambase, np.uint8)
        
        
        self.pts = np.array(self.polygon, np.int32)
        self.pts = self.pts.reshape((-1,1,2))
        cv2.fillConvexPoly(self.mask,self.pts,(255))
        cv2.fillConvexPoly(self.maskrgb,self.pts,(255,255,255))
        
        self.p1=self.calcOwnParams1()
        self.p2=self.calcOwnParams2()
        
        self.FPS=fps
        
        if CLASSES=="version_1":
            # Clases Version 1
            self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}
        elif CLASSES=="version_2":
            # Clases Version 2
            self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8, 'scooter':9, 'bicitaxi':10}
        elif CLASSES=="Version_UMV":
            # Clases Version UMV 
            self.clases={'Camion_C1': 0, 'Camion_C2': 1, 'Camion_C3': 2, 'Camion_C4': 3, 'Camion_C5': 4, 'Camion_C6': 5, 'Auto': 6, 'Colectivo': 7, 'Bus': 8}
        

        # Clases Version 1 
        #self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}
        
        # Clases Version 2
        #self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8, 'scooter':9, 'bicitaxi':10}
        
        # Clases Version UMV 
        #self.clases={'Camion_C1': 0, 'Camion_C2': 1, 'Camion_C3': 2, 'Camion_C4': 3, 'Camion_C5': 4, 'Camion_C6': 5, 'Auto': 6, 'Colectivo': 7, 'Bus': 8}
        
        
    def calcOwnParams1(self): #line's equation Params computation
        return self.calcParams(self.point1,self.point2)

    def calcOwnParams2(self): #line's equation Params computation
        return self.calcParams(self.point3,self.point4)
    
    def calcParams(self,point1, point2): #line's equation Params computation
            if point2[1] - point1[1] == 0:
                 a = 0
                 b = -1.0
            elif point2[0] - point1[0] == 0:
                a = -1.0
                b = 0
            else:
                a = float(point2[1] - point1[1]) / float(point2[0] - point1[0])
                b = -1.0
            
            c = (-a * point1[0]) - b * point1[1]
            #print ('parametros trayecto',a,b,c)
            return self.Params(a,b,c) 
    
    def pointInside(self,point):
        dist=cv2.pointPolygonTest(self.pts,point,True)
        
        if dist>=0:
            return True
        else:
            return False
            
    def listPointsInside(self,listpoints):
        try:
            for point in listpoints:#recorra la lista de puntos
                dist=cv2.pointPolygonTest(self.pts,point,True)
                if dist>=0:
                    return True
        except:
            return False
        return False
        
    def esComparendiable(self,clase):
        if clase=="particular" or clase=="taxi" or clase =="minivan":
            return True
        return False


class conditionalCounter():
    def __init__(self, pt1,pt2,pt3,pt4,filename="salidaconteo.csv",fps=20,linecount=1):
        """
        Inicializacion\n
        Clase conditionalCounter \n
        Esta clase lista todos los Metodos para generar la clase de conteo condicional \n
        Ella genera al inicio los llamados a las clases internas objects y paths,\n
        \n
        La clase objects sirve para llevar registro de los objetos detectados en el cuadro actual\n
        La clase paths sirve para llevar registro del trajecto asociado a cada objeto detectado\n
    
        los metodos son: \n
            __init__ \n
            calcOwnParams \n
            calcParams \n
            testLine \n
            intersectPoint \n
            addToLineCounter \n
            writeToLineCounter \n
            
            SaveLine \n
            LoadLine \n
            
            printPaths \n
            clearObjets \n
            clearPaths \n
            processObjectstoPaths \n
            
            __areLinesIntersecting
            __returnIntersectPoint
            
        \n
        USO:\n
        \n
        pedir puntos de conteo\n
        procesar si trajecto pasa linea de conteo\n
        profit\n
            
        
        
        
        LLAMADO:\n
        
        
            \n
        EJEMPLOS:\n
         
        """
        self.Params = collections.namedtuple('Params', ['a','b','c']) #para guardar la ecuacion de una linea
        
        self.point1 = pt1
        self.point2 = pt2
        self.point3 = pt3
        self.point4 = pt4
        
        self.param1=self.calcL1Params()
        self.param2=self.calcL2Params()
        
        self.conteo=0

        filenameraw, file_extension = os.path.splitext(filename)
        
        self.filename_output=filenameraw+'_lineaCondicional_'+str(linecount)+'.csv'
        self.filename_output_line=filenameraw+'_lineaCondicional_'+str(linecount)+'.lin'
        
        self.FILE = open(self.filename_output,'w')
        self.FILE.write("etiqueta;acumulado;frame;tiempo;\n")
        self.FPS=fps
        # Clases Version 1 
        #self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}
        
        # Clases Version 2
        self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8, 'scooter':9, 'bicitaxi':10}
        
        # Clases Version UMV 
        #self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}
        self.counterclases=np.zeros(len(self.clases))
        self.counterclases0=np.zeros(len(self.clases))
        self.counterclases1=np.zeros(len(self.clases))
        self.linecount=linecount
        self.linecount1=linecount
        self.linecount2=linecount+10
        self.sav=saveAndLoadParser(self.filename_output_line)

        
    def addToLineCounter(self,label,frame,tiempo):
        self.counterclases[self.clases[label]]+=1
        """
        if direct:
            self.counterclases0[self.clases[label]]+=1
        else:
            self.counterclases1[self.clases[label]]+=1
        """
        self.writeToLineCounter(label,self.counterclases[self.clases[label]],frame,tiempo)
        
    def saveFinalCounts(self,frame):
        self.FILE.write("\n")
        self.FILE.write("\n")
        self.FILE.write("Conteo definitivo;ambos sentidos\n")
        self.FILE.write("etiqueta;conteo;tiempo;\n")
        for jj in range(len(self.counterclases)):
            self.FILE.write(str(num2clases[jj])+';'+str(self.counterclases[jj])+';'+str(float(frame)/float(self.FPS))+'\n')
        """
        self.FILE.write("\n")
        self.FILE.write("\n")
        self.FILE.write("Conteo definitivo;direccion positiva\n")
        self.FILE.write("etiqueta;conteo;tiempo;\n")
        for jj in range(len(self.counterclases1)):
            self.FILE.write(str(num2clases[jj])+';'+str(self.counterclases1[jj])+';'+str(float(frame)/float(self.FPS))+'\n')

        self.FILE.write("\n")
        self.FILE.write("\n")
        self.FILE.write("Conteo definitivo;direccion negativa\n")
        self.FILE.write("etiqueta;conteo;tiempo;\n")
        for jj in range(len(self.counterclases0)):
            self.FILE.write(str(num2clases[jj])+';'+str(self.counterclases0[jj])+';'+str(float(frame)/float(self.FPS))+'\n')
        """
        self.FILE.write("Fin de archivo;\n")
        self.FILE.write("AYUDA;manual  ; en ;https://docs.google.com/document/d/1Y2eYLjje2taNnJwVAONLIpsGVm4aj8_jssrNITejFd0/edit?usp=sharing\n")

        
        
    def writeToLineCounter(self,label,count, frame,tiempo):# the input is the class type, the total accumulated count of that class and the frame in wich the object cross the line
        self.FILE.write(str(label)+';'+str(count)+';'+str(tiempo)+';'+str(frame)+'\n')




    def testLines(self,pt1,pt2):
        line_params=self.calcParams(pt1,pt2)
        t1=self.areLinesIntersecting(self.param1,self.point1,self.point2,line_params,pt1,pt2)
        t2=self.areLinesIntersecting(self.param2,self.point3,self.point4,line_params,pt1,pt2)
        if t1 or t2:
            print("t1=",t1,"t2=",t2)
            return True
        return False
    
    def testLine1(self,pt1,pt2):
        line_params=self.calcParams(pt1,pt2)
        return self.areLinesIntersecting(self.param1,self.point1,self.point2,line_params,pt1,pt2)
    
    def testLine2(self,pt1,pt2):
        return self.areLinesIntersecting(self.param2,self.point3,self.point4,self.calcParams(pt1,pt2),pt1,pt2)
        
    

    def areLinesIntersecting(self, params1,pl1,pl2, params2, point1, point2):
        det = float(params1.a) * float(params2.b) - float(params2.a) * float(params1.b)
        if det == 0:
            return False #lines are parallel
        else:
            x = float(params2.b * -params1.c - params1.b * -params2.c)/float(det)
            y = float(params1.a * -params2.c - params2.a * -params1.c)/float(det)
            #x y y son el punto de interseccion ahora toca ver si esta dentro o fuera de los dos puntos.
            if x <= max(point1[0],point2[0]) and x >= min(point1[0],point2[0]) and y <= max(point1[1],point2[1]) and y >= min(point1[1],point2[1]) and x <= max(pl1[0],pl2[0]) and x >= min(pl1[0],pl2[0]) and y <= max(pl1[1],pl2[1]) and y >= min(pl1[1],pl2[1]):
                return True #lines are intersecting inside the line segment
            else:
                return False #lines are intersecting but outside of the line segment

    def calcL1Params(self): #line's equation Params computation
        return self.calcParams(self.point1,self.point2)
    
    def calcL2Params(self): #line's equation Params computation
        return self.calcParams(self.point3,self.point4)

    def calcParams(self,point1, point2): #line's equation Params computation
            if point2[1] - point1[1] == 0:
                 a = 0
                 b = -1.0
            elif point2[0] - point1[0] == 0:
                a = -1.0
                b = 0
            else:
                a = float(point2[1] - point1[1]) / float(point2[0] - point1[0])
                b = -1.0
            
            c = (-a * point1[0]) - b * point1[1]
            #print ('parametros trayecto',a,b,c)
            return self.Params(a,b,c)
            
            
    def intersectPoint1(self,pt1,pt2):
        line_params=self.calcParams(pt1,pt2)
        return self.returnIntersectPoint(self.param1,line_params,pt1,pt2)
        
    def intersectPoint2(self,pt1,pt2):
        line_params=self.calcParams(pt1,pt2)
        return self.returnIntersectPoint(self.param2,line_params,pt1,pt2)

    def returnIntersectPoint(self,params1, params2, point1, point2):
        det = float(params1.a) * float(params2.b) - float(params2.a) * float(params1.b)
        if det == 0:
            return False #lines are parallel
        else:
            x = float(params2.b * -params1.c - params1.b * -params2.c)/float(det)
            y = float(params1.a * -params2.c - params2.a * -params1.c)/float(det)
            return (int(x),int(y))

class counter:
    
    def __init__(self, pt1,pt2,filename="salidaconteo.csv",fps=20,linecount=1):
        """
        Inicializacion\n
        Clase counter \n
        Esta clase lista todos los Metodos para generar la clase de conteo \n
        Ella genera al inicio los llamados a las clases internas objects y paths,\n
        \n
        La clase objects sirve para llevar registro de los objetos detectados en el cuadro actual\n
        La clase paths sirve para llevar registro del trajecto asociado a cada objeto detectado\n
    
        los metodos son: \n
            __init__ \n
            calcOwnParams \n
            calcParams \n
            testLine \n
            intersectPoint \n
            addToLineCounter \n
            writeToLineCounter \n
            
            SaveLine \n
            LoadLine \n
            
            printPaths \n
            clearObjets \n
            clearPaths \n
            processObjectstoPaths \n
            
            __areLinesIntersecting
            __returnIntersectPoint
            
        \n
        USO:\n
        \n
        pedir puntos de conteo\n
        procesar si trajecto pasa linea de conteo\n
        profit\n
            
        
        
        
        LLAMADO:\n
        
        
            \n
        EJEMPLOS:\n
         
        """
        self.Params = collections.namedtuple('Params', ['a','b','c']) #para guardar la ecuacion de una linea
        self.point1 = pt1
        self.point2 = pt2
        
        self.p1=self.calcOwnParams()
        
        self.conteo=0

        filenameraw, file_extension = os.path.splitext(filename)
        
        self.filename_output=filenameraw+'_linea_'+str(linecount)+'.csv'
        self.filename_output_line=filenameraw+'_linea_'+str(linecount)+'.lin'
        
        self.FILE = open(self.filename_output,'w')
        self.FILE.write("etiqueta;acumulado;frame;tiempo;\n")
        self.FPS=fps
        if CLASSES=="version_1":
            # Clases Version 1
            self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}
        elif CLASSES=="version_2":
            # Clases Version 2
            self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8, 'scooter':9, 'bicitaxi':10}
        elif CLASSES=="Version_UMV":
            # Clases Version UMV 
            self.clases={'Camion_C1': 0, 'Camion_C2': 1, 'Camion_C3': 2, 'Camion_C4': 3, 'Camion_C5': 4, 'Camion_C6': 5, 'Auto': 6, 'Colectivo': 7, 'Bus': 8}
        
        # Clases Version 1 
        #self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8}
        
        # Clases Version 2
        #self.clases={'peaton': 0, 'particular': 1, 'taxi': 2, 'motociclista': 3, 'bus': 4, 'camion': 5, 'minivan': 6, 'ciclista': 7, 'tractomula': 8, 'scooter':9, 'bicitaxi':10}
        
        # Clases Version UMV 
        #self.clases={'Camion_C1': 0, 'Camion_C2': 1, 'Camion_C3': 2, 'Camion_C4': 3, 'Camion_C5': 4, 'Camion_C6': 5, 'Auto': 6, 'Colectivo': 7, 'Bus': 8}
        
        self.counterclases=np.zeros(len(self.clases))
        self.counterclases0=np.zeros(len(self.clases))
        self.counterclases1=np.zeros(len(self.clases))
        self.linecount=linecount
        self.sav=saveAndLoadParser(self.filename_output_line)
        

    def __del__(self):
        self.FILE.close()
    
    def saveLine(self):
        self.sav.resetFile()
        self.sav.writeData("punto1",list(self.point1))
        self.sav.writeData("punto2",list(self.point2))
        """
        self.sav.writeData("filename_output",self.filename_output)
        self.sav.writeData("filename_output_line",self.filename_output_line)
        self.sav.writeData("FPS",self.FPS)
        """
        
    def LoadLine(self):
        
        self.sav.openFileToRead()

        tipo,nombre,dat=self.sav.readData()
        print ("Se carga punto de tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))
        self.point1=dat

        tipo,nombre,dat=self.sav.readData()
        print ("Se carga punto de tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))
        self.point2=dat

        
    def addToLineCounter(self,label,frame,tiempo,direct):
        self.counterclases[self.clases[label]]+=1
        if direct:
            self.counterclases0[self.clases[label]]+=1
        else:
            self.counterclases1[self.clases[label]]+=1
            

        self.writeToLineCounter(label,self.counterclases[self.clases[label]],frame,tiempo)
        
    def writeToLineCounter(self,label,count, frame,tiempo):# the input is the class type, the total accumulated count of that class and the frame in wich the object cross the line
        self.FILE.write(str(label)+';'+str(count)+';'+str(tiempo)+';'+str(frame)+'\n')

    def saveFinalCounts(self,frame):
        self.FILE.write("\n")
        self.FILE.write("\n")
        self.FILE.write("Conteo definitivo;ambos sentidos\n")
        self.FILE.write("etiqueta;conteo;tiempo;\n")
        for jj in range(len(self.counterclases)):
            self.FILE.write(str(num2clases[jj])+';'+str(self.counterclases[jj])+';'+str(float(frame)/float(self.FPS))+'\n')

        self.FILE.write("\n")
        self.FILE.write("\n")
        self.FILE.write("Conteo definitivo;direccion positiva\n")
        self.FILE.write("etiqueta;conteo;tiempo;\n")
        for jj in range(len(self.counterclases1)):
            self.FILE.write(str(num2clases[jj])+';'+str(self.counterclases1[jj])+';'+str(float(frame)/float(self.FPS))+'\n')

        self.FILE.write("\n")
        self.FILE.write("\n")
        self.FILE.write("Conteo definitivo;direccion negativa\n")
        self.FILE.write("etiqueta;conteo;tiempo;\n")
        for jj in range(len(self.counterclases0)):
            self.FILE.write(str(num2clases[jj])+';'+str(self.counterclases0[jj])+';'+str(float(frame)/float(self.FPS))+'\n')
        self.FILE.write("Fin de archivo;\n")
        self.FILE.write("AYUDA;manual  ; en ;https://docs.google.com/document/d/1Y2eYLjje2taNnJwVAONLIpsGVm4aj8_jssrNITejFd0/edit?usp=sharing\n")

    def calcOwnParams(self): #line's equation Params computation
        return self.calcParams(self.point1,self.point2)

    def calcParams(self,point1, point2): #line's equation Params computation
            if point2[1] - point1[1] == 0:
                 a = 0
                 b = -1.0
            elif point2[0] - point1[0] == 0:
                a = -1.0
                b = 0
            else:
                a = float(point2[1] - point1[1]) / float(point2[0] - point1[0])
                b = -1.0
            
            c = (-a * point1[0]) - b * point1[1]
            #print ('parametros trayecto',a,b,c)
            return self.Params(a,b,c)

    def __areLinesIntersecting(self,params1, params2, point1, point2):
        det = float(params1.a) * float(params2.b) - float(params2.a) * float(params1.b)
        if det == 0:
            return False #lines are parallel
        else:
            x = float(params2.b * -params1.c - params1.b * -params2.c)/float(det)
            y = float(params1.a * -params2.c - params2.a * -params1.c)/float(det)
            #x y y son el punto de interseccion ahora toca ver si esta dentro o fuera de los dos puntos.
            if x <= max(point1[0],point2[0]) and x >= min(point1[0],point2[0]) and y <= max(point1[1],point2[1]) and y >= min(point1[1],point2[1]) and x <= max(self.point1[0],self.point2[0]) and x >= min(self.point1[0],self.point2[0]) and y <= max(self.point1[1],self.point2[1]) and y >= min(self.point1[1],self.point2[1]):
                return True #lines are intersecting inside the line segment
            else:
                return False #lines are intersecting but outside of the line segment

    def testLine(self,pt1,pt2):
        line_params=self.calcParams(pt1,pt2)
        return self.__areLinesIntersecting(self.p1,line_params,pt1,pt2)

    def intersectPoint(self,pt1,pt2):
        line_params=self.calcParams(pt1,pt2)
        return self.__returnIntersectPoint(self.p1,line_params,pt1,pt2)

    def __returnIntersectPoint(self,params1, params2, point1, point2):
        det = float(params1.a) * float(params2.b) - float(params2.a) * float(params1.b)
        if det == 0:
            return False #lines are parallel
        else:
            x = float(params2.b * -params1.c - params1.b * -params2.c)/float(det)
            y = float(params1.a * -params2.c - params2.a * -params1.c)/float(det)
            return (int(x),int(y))

    def crossSign(self,p1,p2):
        u1=self.point1[0]-self.point2[0]
        v1=self.point1[1]-self.point2[1]
        u2=p1[0]-p2[0]
        v2=p1[1]-p2[1]
        s3=u1*v2-u2*v1
        if s3>=0:
            return 1
        else:
            return 0



if __name__ == "__main__":
    
    testrectangle=True
    
    if(testrectangle):
        
        frame = np.zeros((1080,1920,3), np.uint8)
        rectangulopres=selectRect(frame)
        
        zd=zone_detector(rectangulopres.pt1,rectangulopres.pt2,rectangulopres.pt3,rectangulopres.pt4,frame)
        
        
        cv2.namedWindow('mask')
        cv2.namedWindow('mask rgb')
        
        
        cv2.imshow('mask',zd.mask)
        cv2.imshow('mask rgb',zd.maskrgb)
        
        cv2.waitKey(0)
        
        cv2.destroyWindow('mask')
        cv2.destroyWindow('mask rgb')
        cv2.waitKey(30)
            
    else:
        cv2.namedWindow('frame')
        frame = np.zeros((240,320,3), np.uint8)
        
        
        lineaconteo=selectLine(frame,ownString='Seleccione linea de conteo')    
        
        cv2.circle(frame,lineaconteo.pt1,3,(0,0,255),-1)
        cv2.line(frame,lineaconteo.pt1,lineaconteo.pt2,(0,0,255),1)
        cv2.circle(frame,lineaconteo.pt2,3,(255,0,255),-1)
        
        linept1=lineaconteo.pt1
        linept2=lineaconteo.pt2
        
        
        
        
        lineacarrito=selectLine(frame)    
        
        last_centroid = lineacarrito.pt1
        centroid = lineacarrito.pt2
        
        
        ### EJEMPLO DE USO: 1 SE INICIALIZA LA LINEA A CONTAR
        contar=counter(linept1,linept2)    
    
    
    
    
        while(1):
            cv2.circle(frame,last_centroid,4,(0,255,0), -1) #last_centroid
            cv2.circle(frame,centroid,4,(0,255,0), -1) #current centroid
            cv2.line(frame,last_centroid,centroid,(0,0,255),1) #segment line between car centroid at t-1 and t
            
            cv2.line(frame,linept1,linept2,(200,200,0),2) #intercepting line
            
            ### EJEMPLO DE USO: 2 se usa testline para dar dos puntos a probar si hacen parte o no de la linea
            print("Are Lines Intersecting  1: ",contar.testLine(last_centroid,centroid)," sign ", contar.crossSign(last_centroid,centroid))
            cv2.circle(frame,contar.intersectPoint(last_centroid,centroid),4,(255,255,255), -1) #intersecting point
            
            #print("Are Lines Intersecting  2: ",contar.testLine(centroid,last_centroid))
            #cv2.circle(frame,contar.intersectPoint(centroid,last_centroid),4,(0,0,255), -1) #intersecting point
            
            
            cv2.imshow('frame',frame)
            if cv2.waitKey(2000) & 0xFF == ord('q'):
                break
            
        
        contar.saveLine
    
    
    
    
        while(1):
            cv2.circle(frame,last_centroid,4,(0,255,0), -1) #last_centroid
            cv2.circle(frame,centroid,4,(0,255,0), -1) #current centroid
            cv2.line(frame,last_centroid,centroid,(0,0,255),1) #segment line between car centroid at t-1 and t
            
            cv2.line(frame,linept1,linept2,(200,200,0),2) #intercepting line
            
            ### EJEMPLO DE USO: 2 se usa testline para dar dos puntos a probar si hacen parte o no de la linea
            print("Are Lines Intersecting  1: ",contar.testLine(last_centroid,centroid)," sign ", contar.crossSign(last_centroid,centroid))
            cv2.circle(frame,contar.intersectPoint(last_centroid,centroid),4,(255,255,255), -1) #intersecting point
            
            #print("Are Lines Intersecting  2: ",contar.testLine(centroid,last_centroid))
            #cv2.circle(frame,contar.intersectPoint(centroid,last_centroid),4,(0,0,255), -1) #intersecting point
            
            
            cv2.imshow('frame',frame)
            if cv2.waitKey(2000) & 0xFF == ord('q'):
                break
    
    
        cv2.destroyAllWindows()
        
        
        
        
        
    
    
    
    
