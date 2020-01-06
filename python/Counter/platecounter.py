 # en base a https://stackoverflow.com/questions/29791075/counting-the-point-which-intercept-in-a-line-with-opencv-python 
import cv2
import numpy as np
import collections
import os


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
        
    def openFileToWrite(self):
        self.FILE = open(self.filename,'a')
        
    def writeLine(self,line):
        self.FILE.write(str(line))
        
    def readLine(self):
        return self.FILE.readline()
        
    def closeFile(self):
        self.FILE.close()




class plateLog:
    def __init__(self,FPS=20,filename="salidaplacas.csv"):
        """
        Inicializacion\n
        Clase counter \n
        Esta clase lista todos los Metodos para generar la clase de PlateLog \n
        La clase objects sirve para llevar registro de las placas detectadas en el video actual\n
    
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
        self.conteo=0
        self.fps=FPS

        filenameraw, file_extension = os.path.splitext(filename)
        
        self.filename_output=filenameraw+'_placas_'+'.csv'
        
        self.sav=saveAndLoadParser(self.filename_output)
        self.sav.resetFile()
        self.sav.appendFile("PLACA;frame;tiempo;linea\n")
        self.data=[]

    def __del__(self):
        self.sav.closeFile()
        
    def addToplateLog(self,plate,frame,tiempo,lin):
        self.data.append((plate,frame,tiempo,lin))
        
    def printPlateLog(self):
        print(self.data)

    def saveFinalplateLog(self,Phelp=True):
        self.__writeToplateLog()
        if Phelp:
            self.sav.appendFile("Fin de archivo;\n")
            self.sav.appendFile("AYUDA;:;manual;en;TODO\n")

    def __writeToplateLog(self):# NO use esta use la de arriba seleccione si quiere ayuda o no
        self.sav.openFileToWrite()
        for reg in self.data:    
            self.sav.writeLine(str(reg[0])+';'+str(reg[1])+';'+str(reg[2])+';'+str(reg[3])+'\n')
        self.sav.closeFile()



if __name__ == "__main__":
    
    pl=plateLog()
    
    pl.addToplateLog("ABC123",12,0.125,1)
    pl.addToplateLog("ABC124",13,0.126,2)
    pl.addToplateLog("ABC125",14,0.127,3)
    pl.addToplateLog("ABC126",15,0.128,4)
    pl.addToplateLog("ABC127",16,0.129,1)
    
    
    pl.printPlateLog()
    pl.saveFinalplateLog()
    
    
    
    
