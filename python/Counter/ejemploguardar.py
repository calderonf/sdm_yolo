# -*- coding: utf-8 -*-
"""
Created on Sun May 27 11:16:37 2018

@author: francisco
"""

class saveAndLoadParser:
    
    def __init__(self, filename="archivoPorDefecto.txt"):
        self.filename=filename
        
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
            return -1,-1,-1
        if mystr=='\n':
            return 0,0,0
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
            return -1,-1,-1        
        return tipo,nombre,datos

data = [0,1,2,3,4,5]
string='filename'
floatnumber=3.1415926535
integer=850508


sv=saveAndLoadParser("borrartest.lin")

sv.resetFile()
sv.writeData("suenio","mucho")
sv.writeData("ojos",2)
sv.writeData("lista",[1,2,3,4,5,6,7,8,9])
sv.writeData("pi",3.1415926535)



sv.openFileToRead()

tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))


tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))

tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))

tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))

tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))


tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))


tipo,nombre,dat=sv.readData()

print ("Datos son tipo:"+str(tipo)+" de nombre:"+str(nombre)+" con los datos:"+str(dat))

"""
with open("test.txt", "w") as file:
    file.write('list='+str(data)+'\n')
    file.write('string='+str(string)+'\n')
    file.write('double='+str(floatnumber)+'\n')
    file.write('int='+str(integer)+'\n')

with open("test.txt", "r") as file:
    mystr=file.readline()
    ln=mystr.split('=')
    data1 = eval(ln[1])
    mystr=file.readline()
    ln=mystr.split('=')
    data2 = ln[1].rstrip()
    mystr=file.readline()
    ln=mystr.split('=')
    data3 = eval(ln[1])
    mystr=file.readline()
    ln=mystr.split('=')
    data4 = eval(ln[1])

# Let's see if data and types are same.
print(data, type(data), type(data[0]))
print(data1, type(data1), type(data1[0]))


print(string, type(string), type(string[0]))
print(data2, type(data2), type(data2[0]))


print(floatnumber, type(floatnumber))
print(data3, type(data3))


print(integer, type(integer))
print(data4, type(data4))
"""