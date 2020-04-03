#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Francisco Carlos Calderon
Created on 4/01/18   4:33PM 2018


Este modulo implementa llamados de estructuras de seguimiento\n 
puede ser llamado desde esta misma carpeta o invocado como un modulo aparte\n


Para generar la documentacion del modulo ejecute desde una terminal en el directorio raiz del modulo:\n

  python -m pydoc -w tracking\n
  
  A continuacion se listan prerequisitos o 'modulos',  clases y funciones implementadas.\n
  
"""

import os
import sys
import math
import random
import numpy as np
from threading import Thread
#import RPi.GPIO as GPIO
from time import sleep
from time import gmtime, strftime


OPENCVSUPPORT=True
if OPENCVSUPPORT:
    import cv2

CLASSES="version_2"

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









#DefaultTTL=10 #Tiempo de vida por default de cada estructura de seguimiento 
#definiciones



def getMinItem(a):
    """
    Funcion de uso general que busca el menor de una lista y retorna su id y valor
    """
    
    idx=min(range(len(a)), key=a.__getitem__)    
    return (idx,a[idx])
    
    
class point:
    """
    Clase point para guardar la estructura de un punto. posiblemente \n
    se le pueda generar una funcion de distancia entre puntos\n
    """
    def __init__(self, x, y):
        """
        Inicializacion\n
        """
        self.x = x
        self.y = y
    def retPoint(self):
        """
        Funcion que retorna la pareja ordenada, util para usar en conjunto con cv2\n
        """
        return (self.x,self.y)
class cont:
    """
    Clase cont de contenedor o tamanio de rectangulo contenedor\n
    """
    def __init__(self, w, h):
        """
        Inicializacion\n
        """
        self.w = w
        self.h = h
        
class rect:
    """
    Clase de rectangulo, que contiene dos puntos, [x,y] y [u,v] con \n
    las esquinas del rectangulo contenedor\n
    """
    def __init__(self, x, y, u, v):
        """
        Inicializacion\n
        """
        self.x = x
        self.y = y
        self.u = u
        self.v = v
    def retPoints(self):
        """
        Funcion que retorna dos parejas ordenadas, util para usar en conjunto con cv2\n
        """
        return ((self.x,self.y),(self.u,self.v))

class singleobject:
    """
    Clase de objeto simple con un punto, un tamanio de rectangulo contenedor y sus aristas\n
    """
    def __init__(self, x,y,w,h,strFeature):
        self.cp=point(x,y)
        self.tam=cont(w,h)
        self.rect=rect(x-w/2,y-h/2,x-w/2+w,y-h/2+h)# en notacion para cv2.rectangle(imgFile3, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
        self.str=strFeature

class objects:
    """
    Clase de multiples objetos simples, cada uno con: un punto, \n
    un tamanio de rectangulo contenedor y sus aristas\n
    """
    def __init__(self):
        """
        inicializacion de lista con objetos
        """
        self.obs=[]
        
    def insertObjet(self,x,y,w,h,strFeature):
        """
        Funcion para insertar un objeto nuevo a la lista, se usa append \n
        por lo que los objetos se listan de cola a cabeza, el mas reciente queda al final\n
        """
        ob=singleobject(x,y,w,h,strFeature)
        self.obs.append(ob)
        
    def printObjets(self):
        """
        Funcion para imprimir la lista de objetos en pantalla \n
        util para debug\n
        """
        temp=1
        print ('\nImprimiendo '+str(len(self.obs))+' objetos: \n::::::::::::::::::::::')
        for obj in self.obs[:]:
            print (' Objeto numero '+str(temp)+'  '+' Con etiqueta :'+str(obj.str))
            temp=temp+1
            print ('  Centro en ['+str(obj.cp.x)+','+str(obj.cp.y)+']')
            print( '  Tamanio : w='+str(obj.tam.w)+', h='+str(obj.tam.h))
            print( '  Rectangulo: desde ['+str(obj.rect.x)+','+str(obj.rect.y)+']'+' \n              hasta ['+str(obj.rect.u)+','+str(obj.rect.v)+']')
            print( '  ....................')

    def clearObjets(self):
        """
        Funcion para eliminar el contenido total de la lista de objetos\n
        \n
        """
        del self.obs[:]
        
class singlepath:
    """
    Clase con un trayecto, que contiene una estructura de seguimiento completa. \n
    """
    def __init__(self, idx,x,y,w,h,framesttl,featurestring,lineasconteo=10,lineasconteocondicional=20):
        
        #adicion seleccion de clase por estimacion modal
        self.counterclases=np.zeros(len(clases))
        self.counterclases[clases[featurestring]]+=1
        self.str=featurestring# La primera vez se le agrega 1 y se deja por defecto en esa clase. 
        
        self.idx=idx
        self.cp=point(x,y)#punto central mas reciente
        self.tam=cont(w,h)# tamanio mas reciente
        self.rect=rect(x-w/2,y-h/2,x-w/2+w,y-h/2+h)# en notacion para cv2.rectangle(imgFile3, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
        self.path=[]
        self.path.append(point(x,y))
        self.ttl=framesttl
        self.colour=(int(random.uniform(0,255)),int(random.uniform(0,255)),int(random.uniform(0,255)))
        self.contado=False
        self.contadores=np.zeros(lineasconteo)
        self.contadocondicional=False
        
        self.contadoresCondicionales=np.zeros(lineasconteocondicional)
        self.direccionCondicional=0
        #contadoresCondicionales
        #adicion cebra
        self.puntosFrontera=[(x,y),(x-w/2,y-h/2),(x-w/2+w,y-h/2+h),(x-w/2,y-h/2+h),(x-w/2+w,y-h/2)]
        self.contadorCebra=0
        self.detectadoCebra=False
        
        
class paths:
    """
    Clase de multiples paths o trajectos simples, cada uno con: un punto, \n
    un tamanio de rectangulo contenedor y sus aristas\n
    """
    def __init__(self):
        """
        Inicializacion de una lista de paths simples
        """
        self.p=[]
        
        
    def createNewPath(self,idx,x,y,w,h,framesttl,featurestring):
        """
        Funcion para insertar un path o trayecto nuevo a la lista, se usa append \n
        por lo que los trayectos se listan de cola a cabeza, el mas reciente queda al final\n
        """
        ob=singlepath(idx,x,y,w,h,framesttl,featurestring)
        self.p.append(ob)
        
    def insertToPath(self,idx,x,y,w,h,st,framesttl):
        """
        Funcion para insertar a un trayecto o path existente un nuevo punto\n
        si el id del trayecto o path no existe retorna 1, si existe retorna 0\n
        por lo que su uso recomendado es:\n
        if self.insertToPath(idx,x,y,w,h):#si no existe\n
            print('ERROR: el id '+str(idx)+' no existe en la lista de trayectos')\n
        
        """
        for find in self.p[:]:
            if idx==find.idx:
                #si es el id que es
                find.cp.x=x
                find.cp.y=y
                find.tam.w=w# tamanio mas reciente
                find.tam.h=h# tamanio mas reciente
                find.rect.x=x-w/2
                find.rect.y=y-h/2
                find.rect.u=x-w/2+w
                find.rect.v=y-h/2+h
                find.path.append(point(x,y))
                find.ttl=framesttl
                
                find.counterclases[clases[st]]+=1
                find.str=num2clases[find.counterclases.argmax()]# se busca la clase que tenga mayor numero de conteos MEJORA SI TIENE LOS MISMOS PONER LOS DOS
        
                #adicion cebra
                find.puntosFrontera=[(x,y),(x-w/2,y-h/2),(x-w/2+w,y-h/2+h),(x-w/2,y-h/2+h),(x-w/2+w,y-h/2)]
                
                
                return 0
        print ('WARNING: could not find the idx '+str(idx)+' in the path list please check for possible errors'  )  
        return 1    
            
    def printPath(self,path):
        """
        Funcion que Imprime todos los puntos que hacen parte de un trayecto \n
        en una sola linea\n
        """
        pathcompleto=False
        if pathcompleto:
            print ('  Trayectoria:')
            sys.stdout.write('  |->')
            for l in path[:]:
                sys.stdout.write('['+str(l.x)+','+str(l.y)+']->') 
            sys.stdout.write(' *\n')
        else:
            print ('  Trayectoria de tamanio: '+str(len(path[:])))
        
    def printPaths(self):
        """
        Funcion que Imprime todos los trayectos junto con su secuencia de puntos, y sus propiedades\n
        """
        temp=1
        print ('\nImprimiendo '+str(len(self.p))+' trajectorias: \n++++++++++++++++++++++')
        for pat in self.p[:]:
            print (' Trajectoria numero '+str(temp)+'.  '+' Con id='+str(pat.idx)+'.  '+' Con etiqueta :'+str(pat.str))
            temp=temp+1
            print ('  Centro en ['+str(pat.cp.x)+','+str(pat.cp.y)+']')
            print ('  Tamanio : w='+str(pat.tam.w)+', h='+str(pat.tam.h))
            print ('  Rectangulo: desde ['+str(pat.rect.x)+','+str(pat.rect.y)+']'+' \n              hasta ['+str(pat.rect.u)+','+str(pat.rect.v)+']')
            print ('  Tiempo de vida TTL='+str(pat.ttl)  )
            self.printPath(pat.path)
            print ('  --------------------')
            
    def clearPaths(self):
        """
        Funcion que borra la lista de trayectos\n
        """
        del self.p[:]
            
    
class tracking:
    """
    Clase tracking \n
    Esta clase lista todos los Metodos para generar la clase de seguimiento \n
    Ella genera al inicio los llamados a las clases internas objects y paths,\n
    \n
    La clase objects sirve para llevar registro de los objetos detectados en el cuadro actual\n
    La clase paths sirve para llevar registro del trajecto asociado a cada objeto detectado\n

    los metodos son: \n
        __init__ \n
        insertNewObject \n
        insertNewPath \n
        insertToPath \n
        printObjets \n
        printPaths \n
        clearObjets \n
        clearPaths \n
        processObjectstoPaths \n
        
        __euclidean
        __safe_div
        __avgsize
        __calcPeso
        __calcPesos
    \n
    USO:\n
    \n
    llenar objetos\n
    procesar objetos\n
    profit\n
        
    
    
    
    LLAMADO:\n
    
    
        \n
    EJEMPLOS:\n
     
    """
    def __init__(self,verbose=False,mindist=100,framesttl=30):#
        """
        Funcion de inicializacion simplementa llamma a las clases objects y paths\n
        """
        self.framesttl=framesttl
        self.verbose=verbose
        self.__COSTOMINASIGNACION=mindist#100 pixeles es un buen valor para iniciar
        self.idx=long(1)
        self.o=objects()
        self.p=paths()
        
        
    def insertNewObject(self,x,y,w,h,strFeature='Objeto'):
        """
        Funcion que inserta un nuevo objeto a la lista de objetos actuales a seguir\n
        """
        self.o.insertObjet(x,y,w,h,strFeature)
        
    def insertNewPath(self,idx,x,y,w,h,featurestring='Objeto'):
        """
        Funcion que inserta un nuevo trayecto a la lista\n
        """
        self.p.createNewPath(idx,x,y,w,h,self.framesttl,featurestring)
        
    def insertToPath(self,idx,x,y,w,h,st):
        """
        Funcion que inserta un nuevo punto a la trayectoria ya existente\n
        si el id del trayecto o path no existe retorna 1, si existe retorna 0\n
        por lo que su uso recomendado es:\n
        if self.p.insertToPath(idx,x,y,w,h):#si no existe\n
            print('ERROR: el id '+str(idx)+' no existe en la lista de trayectos')\n
        """
        return self.p.insertToPath(idx,x,y,w,h,st,self.framesttl)
    
    def printObjets(self):
        """
        Funcion que imprime la lista de objetos y sus propiedades\n
        """
        self.o.printObjets()
    
    def printPaths(self):
        """
        Funcion que imprime la lista de paths y sus propiedades\n
        """
        self.p.printPaths()
        
    def clearObjets(self):
        """
        Funcion que borra la lista de objetos,\n
        esta toca borrarla antes de analizar cada cuadro\n
        """
        self.o.clearObjets()
                
        
    def clearPaths(self):
        """
        Funcion que borra la lista de trayectos \n
        OJO esta no es tan bueno irla borrando por lo que no se recomienda su uso\n
        """
        self.p.clearPaths()
        
    def __euclidean(self,io,ip):
        """
        Calcula la distancia euclideana entre un objeto y la ultima pos de un trayecto determinado
        los puntos entan en:
        self.o.obs[io].cp
        self.p.p[ip].cp
        """
        return math.sqrt(pow(self.o.obs[io].cp.x-self.p.p[ip].cp.x,2)+pow(self.o.obs[io].cp.y-self.p.p[ip].cp.y,2))
    def __safe_div(self,x,y):
        """
        Funcion super simple que evita divisiones por cero
        """
        if y == 0:
            print ('ERROR division por cero encontrada por favor revise')
            return 0
        return float(x) / float(y)
        
        
    def __avgsize(self,io,ip):
        """
        Calcula la diferencia de tamanio entre un objeto, y el ultimo objeto registrado en un trayecto
        los tamanios estan en:
        self.o.obs[io].tam
        self.p.p[ip].tam
        
        """
        wo=self.o.obs[io].tam.w
        ho=self.o.obs[io].tam.h
        
        wp=self.p.p[ip].tam.w
        hp=self.p.p[ip].tam.h
        
        # este tamanio lo mejor es tratarlo como otra dimension, en la que simplemente se calcula una norma
        # luego, se normaliza y se le suma al costo solamente para penalizar diferencias muy grandes en tamanio como nuevos objetos
        
        return math.sqrt(pow(self.__safe_div((wo-wp),max(abs(wo),abs(wp))),2)+pow(self.__safe_div((ho-hp),max(abs(ho),abs(hp))),2))
        

    def __calcPeso(self,io,ip):
        """
        Funcion que retorna un escalar con el peso entre un objeto y un trayecto en particular\n
        esta es la funciona mas sensible a cambios y sujeta a mejoras, ya que de este pesos de \n
        desprende la funcion discreta a minimizar\n
        
        class singleobject:
            def __init__(self, x,y,w,h):
                self.cp=point(x,y)
                self.tam=cont(w,h)
                self.rect=rect(x-w/2,y-h/2,x-w/2+w,y-h/2+h)# en notacion para cv2.rectangle(imgFile3, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)

        class singlepath:
            def __init__(self, idx,x,y,w,h,framesttl):
                self.idx=idx
                self.cp=point(x,y)#punto central mas reciente
                self.tam=cont(w,h)# tamanio mas reciente
                self.rect=rect(x-w/2,y-h/2,x-w/2+w,y-h/2+h)# en notacion para cv2.rectangle(imgFile3, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
                self.path=[]
                self.path.append(point(x,y))
                self.ttl=self.framesttl
        """
        
        #oo=self.o.obs[io]
        #pp=self.p.p[ip]
        
        #1.Distancias euclideanas entre puntos centrales    
        leng=self.__euclidean(io,ip)
        #2.Diferencias de tamanios entre rectangulos contenedores
        diffsize=self.__avgsize(io,ip)
        
        if leng>0:
            return leng+leng*diffsize   # maximo teorico en leng+sqrt(2)*leng
                                    # minimo teorico en leng
        else:
            print ('io= '+str(io)+' ip= '+str(ip)+' diffsize= '+str(diffsize))
            return diffsize
        
    def __calcPesos(self): 
        """
        Funcion que retorna una matriz de pesos calculados a partir de \n
        la lista de objetos, con una lista de trajectos \n
        la primera dimension son los objetos la segunda los trayectos \n
        """
        to=len(self.o.obs)
        tp=len(self.p.p)
        if (to==0 or tp==0):# si no hay objetos o trayectos retorna una lista vacia 
            pesos=[]
            return pesos
            
        pesos = [[1000000 for x in range(tp)] for y in range(to)]
        # len(pesos) = to = objects
        # len(pesos[0]) = tp = paths
        for io in range (to):
            for ip in range (tp):
               pesos[io][ip]=self.__calcPeso(io,ip)
              
        if self.verbose==True:
            print ('Matriz de pesos: filas objetos = '+str(to)+' columnas trajectos = '+str(tp))
            print('\n'.join( [''.join(['{:16}'.format(item) for item in row]) for row in pesos] ) )      
            
        return pesos
        
        
    def objets2NewPaths(self):
        """
        Funcion que hace que todos los objetos actuales sean \n
        trayector nuevos, solo se cuemple en el caso en que \n
        no existan trayectos anteriores\n
        """
        
        for io in self.o.obs[:]:
            self.insertNewPath(self.idx,io.cp.x,io.cp.y,io.tam.w,io.tam.h,io.str)
            self.idx+=1
    if OPENCVSUPPORT:
        def drawPaths(self,image):
            """
            Funcion que dibuja en la imagen los trayectos creados por un objeto siendo seguido,\n
            """
            
            for ip in self.p.p[:]:
                pt=(int(ip.path[0].x),int(ip.path[0].y))
                cv2.circle(image,pt,2,ip.colour,-1)
                
                pt=(int(ip.path[-1].x),int(ip.path[-1].y))
                cv2.circle(image,pt,2,ip.colour,-1)
                if len(ip.path)>1:
                    for ptr in range(1,len(ip.path)):
                        pt1=(int(ip.path[ptr-1].x),int(ip.path[ptr-1].y))
                        pt2=(int(ip.path[ptr].x),int(ip.path[ptr].y))
                        
                        cv2.line(image,pt1,pt2,ip.colour,thickness=1, lineType=8, shift=0)
                   
                
        
    def processTTL(self):
        """
        Funcion que resta uno a cada elemento de los trayectos,\n
        y cuando se cumple el tiempo de vida o ttl=0 se elimina\n
        """
        for ip in self.p.p[:]:
            ip.ttl-=1
            if ip.ttl<=0:
                if self.verbose:
                    print (20*'*#'+'*')
                    print( ('*Eliminando por ttl path con id = '+str(ip.idx)))
                    print( 20*'*#'+'*')
                self.p.p.remove(ip)
        #for ip in self.p.p[:]:
        
    def __objects2Paths(self,pesos):
        """
        Funcion que analiza la matriz de pesos y genera las asignaciones correspondientes
        """
        if len(pesos)==0:#nada por asignar se sale
            return
        if len(pesos[0])==0:#si hay uno o mas objetos, pero no trayectos, salga este caso ya esta cubierto
            print ('WARNING:: este caso ya estaba cubierto hay un problema extranio revise...'  )          
            return
        no = len(pesos)#numero de objetos
        np = len(pesos[0])#numero de trayectos
        minnonp=min(no,np)
        maxnonp=max(no,np)
        rego = range(no)
        #regp = range(np)      
        
        for nit in range(minnonp):
            minval=[]        
            minvid=[]        
            for o2t in pesos:
                mintuple1=getMinItem(o2t)
                if self.verbose:
                    print (mintuple1)
                minvid.append(mintuple1[0])
                minval.append(mintuple1[1])
            #luego por columnas
            mintuple2=getMinItem(minval)
            
            if self.verbose:
                print ('mintuple2')
                print (mintuple2)
            
            minpath=minvid[mintuple2[0]]
            minobj=mintuple2[0]
            mincost=mintuple2[1]
            if self.verbose:
                print ('minobj')
                print (minobj)
                print ('minpath')
                print (minpath)
            # cuando se tiene toca asignar este objeto a ese path en especial, 
            # siempre y cuando la distancia sea menor a un valor establecido
            # si es mayor a ese valor, se crea un nuevo objeto
            
            if mincost>self.__COSTOMINASIGNACION:
                #como es mayor se crea un nuevo path con este objeto y suma uno al idx
                if self.verbose==True:            
                    print ('se asigna por costo mayor al minimo definido condicion 2: '+20*'2') 
                self.insertNewPath(self.idx,self.o.obs[minobj].cp.x,self.o.obs[minobj].cp.y,self.o.obs[minobj].tam.w,self.o.obs[minobj].tam.h,self.o.obs[minobj].str)
                self.idx+=1
            else:
                #Como es menor se le adiciona al final del path y se reinicia su ttl
                rego.remove(minobj) 
                #regp.remove(minpath)                               
                self.insertToPath(self.p.p[minpath].idx,self.o.obs[minobj].cp.x,self.o.obs[minobj].cp.y,self.o.obs[minobj].tam.w,self.o.obs[minobj].tam.h,self.o.obs[minobj].str)            
                a=1
            # para finalizar se elimina esa fila y columna y se inicia de nuevo ignirando estos objetos y paths ya emparejados. 
            # en ves de eliminar le voy a poner un valor muy grande con eso me evito problemas de indices
            for io in range(no):
                pesos[io][minpath]=1000000
            for ip in range(np):
                pesos[minobj][ip]=1000000
            
            if self.verbose:
                print ('Matriz de pesos: filas objetos = '+str(no)+' columnas trajectos = '+str(np))
                print('\n'.join( [''.join(['{:16}'.format(item) for item in row]) for row in pesos] ) ) 
                
        if len(rego)!=0:
            #si no borro todos los elementos de rego es por que quedan objetos sin emparejar, por lo que deben ser puestos en un nuevo trajecto
            for nob in rego:
                self.insertNewPath(self.idx,self.o.obs[nob].cp.x,self.o.obs[nob].cp.y,self.o.obs[nob].tam.w,self.o.obs[nob].tam.h,self.o.obs[minobj].str)
                self.idx+=1
                
        
        
    def processObjectstoPaths(self):
        """
        Funcion que procesa la lista de objetos insertados\n
        y dependiendo de sus caracteristicas, los asigna a trayectos nuevos o a existentes\n
        al final le quita uno a el TTL y elimina los trayectos viejos\n
        """
        if len(self.o.obs)==0 and len(self.p.p)==0:#si no hay objetos nuevos ni trayectos antiguos salga
            return
        if len(self.p.p)==0:#si no hay trayectos en la lista de trayectos todos los objetos son nuevos inicios de trayecto
            if self.verbose:            
                print ('Condicion 1: '+20*'1')            
            self.objets2NewPaths()#se adicionan como trayectos
            self.clearObjets()#se eliminan
            return
        if len(self.o.obs)==0:#si no hay objetos nuevos a seguir todos los trayectos disminuyen su ttl
            self.processTTL()
            return
            
        #crear matriz de pesos
        pesos=self.__calcPesos()
          
        #asignar objetos a trayectos
        self.__objects2Paths(pesos)
        #eliminar objetos antiguos
        self.clearObjets()#se eliminan
        #descontar TTL
        self.processTTL()
    
        """
    def __calcularPesos(self,filename): 
        """
if __name__ == "__main__":
    """
    print 'probando estructuras de objetos'
    obs=objects()
    obs.insertObjet(2,3,60,80)
    obs.insertObjet(5,7,100,200)
    obs.printObjets()
    obs.clearObjets()
    obs.printObjets()
    print 'probando estructuras de tracking'
    pths=paths()
    pths.createNewPath(1,2,3,4,5)
    pths.createNewPath(2,7,8,9,10)
    pths.createNewPath(3,7,8,9,10)
    pths.printPaths()
    pths.insertToPath(1,1,2,3,4)
    pths.insertToPath(2,1,2,3,4)
    pths.insertToPath(3,1,2,3,4)
    pths.insertToPath(3,1,6,3,4)
    pths.insertToPath(3,9,2,7,4)
    pths.printPaths()
    pths.clearPaths()
    print '//////////BORRANDO/////////////'
    obs.printObjets()
    pths.printPaths()
    print '@@@@@@@ Nueva Prueba @@@@@@@'
    """
    tr=tracking(verbose=True,mindist=100)
    
    tr.insertNewObject(10,10,5,5)
    tr.insertNewObject(2,3,60,80)
    tr.insertNewObject(3,4,5,6)
    tr.insertNewObject(7,2,345,345)

    tr.o.printObjets()

    tr.insertNewPath(1,10,2,3,4)
    tr.insertNewPath(2,234,1324,2134,4)
    tr.insertNewPath(3,7,2,3,4)
    #tr.insertNewPath(4,786,785,65,4)
    #tr.insertNewPath(5,15,2,3,4)
    #tr.insertNewPath(6,1,2,87,4)

    tr.p.printPaths()
    print ('procesando objetos')
    tr.processObjectstoPaths()
    
    tr.p.printPaths()
        
        
