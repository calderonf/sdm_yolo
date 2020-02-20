#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import glob
from PIL import Image
import easygui
from threading import Thread

parallelo=0

class reporte:
    def __init__(self,folder,archivosalida):
        self.fl=open(folder+'/'+archivosalida,'w')
        self.nl='\n'
        self.first_time=True        
        
    def generar_reporte_linea(self,Via_Principal,Via_secundaria,Movimiento,Acceso,Salida,DD,MM,AAAA,periodo):    
        self.leyenda="FECHA,Calle,Carrera,Descripcion,Origen,Destino,Periodo,Peaton,Particular,Taxi,Motociclista,Bus,Camion,Minivan,Ciclista,Tractomula,\n"
        self.periodo=str(periodo)
        self.Via_Principal=Via_Principal
        self.Via_secundaria=Via_secundaria
        self.Movimiento=Movimiento
        self.Acceso=Acceso
        self.Salida=Salida
        self.initlabel=str(DD)+str(MM)+str(AAAA)+','+str(self.Via_Principal)+','+str(self.Via_secundaria)+','+str(self.Movimiento)+','+str(self.Acceso)+','+str(self.Salida)+','+self.periodo+','
        # escribiendo leyenda en archivo si es la primera linea que se escribe en el mismo
        if self.first_time:
            self.fl.write(self.leyenda)
            self.first_time=False
        
    def cerrarArchivo(self):
        self.fl.close()
    
    def actualizarPeriodo(self,DD,MM,AAAA,periodo):
        self.periodo=str(periodo)
        self.initlabel=str(DD)+str(MM)+str(AAAA)+','+str(self.Via_Principal)+','+str(self.Via_secundaria)+','+str(self.Movimiento)+','+str(self.Acceso)+','+str(self.Salida)+','+self.periodo+','

    
    def agregarData(self,Data):
        if len(Data)==9:
            
            self.fl.write(self.initlabel)
            for i in range(9):
                self.fl.write(str(int(float(Data[i][1])))+',') # conteos por etiqueta
            self.fl.write(self.nl)
        else:
            print "ERROR: el tamaño de los datos no es el adecuado"


def retornarNombreLinea(path,nombrevideo,numlinea):
    nombrevideo.rstrip()
    name=nombrevideo.split('.')[0]
    linname=path+'/'+name+'_linea_'+str(numlinea)+'.csv'
    if not os.path.isfile(linname):
        print ("ERROR el archivo "+linname+ "no existe, y se esperaba SALIENDO")
    return linname
    
def getDataFromFile(filelin):
    fh=open(filelin,'r')
    countdata1=[]
    countdata2=[]
    countdata3=[]
    while True:
        # read line
        line = fh.readline()
        #print line
        if not line:
            print "WARNING: saliendo por que se llego al final del archivo posible ERROR"
            break
        
        if line=="\n":
            #print "espacio en blanco detectado"
            continue
        if line.rstrip() == "AYUDA;manual  ; en ;https://docs.google.com/document/d/1Y2eYLjje2taNnJwVAONLIpsGVm4aj8_jssrNITejFd0/edit?usp=sharing":
            break
            #print "saliendo de archivo de manera correcta"
        if line.rstrip() =="Conteo definitivo;ambos sentidos":
            line = fh.readline().rstrip()
            for i in range (9):
                line = fh.readline().rstrip()
                countdata1.append(line.replace(',',';').split(';'))
        
        if line.rstrip() == "Conteo definitivo;direccion positiva":
            line = fh.readline().rstrip()
            for i in range (9):
                line = fh.readline().rstrip()
                countdata2.append(line.replace(',',';').split(';'))
        
        if line.rstrip() == "Conteo definitivo;direccion negativa":
            line = fh.readline().rstrip()
            for i in range (9):
                line = fh.readline().rstrip()
                countdata3.append(line.replace(',',';').split(';'))
    return countdata1,countdata2,countdata3

folder=easygui.diropenbox(title="Seleccione la carpeta con los reportes de videos a unir",default="/Videos")
filelistcsv=glob.glob(folder+"/*.csv")
filelistjpg=glob.glob(folder+"/*.jpg")
filereport=folder+'/'+'merge_video_sources_report.csv'
basewidth = 600
p=[]
#poner el el otro generador de reportes.
if not os.path.isfile(filereport):
    print("ERROR: LA CARPETA NO CONTIENE ARCHIVO DE REPORTE DE VIDEOS INTENTANDO GENERAR")
    import glob
    os.chdir(folder)
    listaarchivos=glob.glob("*.csv")
    FILE_report_w  = open(filereport, 'w') 
    FILE_report_w.write("File_Name;Year;Month;Day;Start_Time;Duration;End_Time\n")
    listaarchivos.sort()  
    
    listalinea1=[]
    cont=1
    for filea in listaarchivos:
        if filea[-5]=="1":
            listalinea1.append(filea)
          
    listalinea1.sort()
    
    for archivo in listalinea1:
        ar_split=archivo.split("_")
        archivo_video=ar_split[0]+"_"+ar_split[1]+"_"+ar_split[2]+".avi"
        ano=ar_split[1][0:4]
        mes=ar_split[1][4:6]
        dia=ar_split[1][6:8]
        start_time=ar_split[1][8:10]+":"+ar_split[1][10:12]+":"+ar_split[1][12:14]
        Duration="05"# para videos de contrato monitoreo la duracion es cada 5 minutos. 
        end_time=ar_split[1][8:10]+":"+ar_split[1][10:12]+":"+ar_split[1][12:14]     
        towrite=archivo_video+";"+ano+";"+mes+";"+dia+";"+start_time+";"+Duration+";"+end_time+"\n"
        FILE_report_w.write(towrite)
        cont+=1
    FILE_report_w.close()

if len(filelistcsv) == 0:
    print("ERROR: LA CARPETA NO CONTIENE ARCHIVOS .csv DE REPORTE SALIENDO")
elif len(filelistjpg) == 0:
    print("ERROR: LA CARPETA NO CONTIENE ARCHIVOS DE LINEA .jpg CON LINEAS DE CONTEO SALIENDO")
elif not os.path.isfile(filereport):
    print("ERROR: LA CARPETA NO CONTIENE ARCHIVO DE REPORTE DE VIDEOS saliendo...")
    
else:
    filelistcsv.sort()
    filelistjpg.sort()
    easygui.msgbox("Se han detectado "+str(len(filelistjpg))+" Lineas de conteo. Se le va a preguntar por cada una de ellas")

    rp=reporte(folder,"reporte_general_carpeta.csv")
    
    for linjpeg in filelistjpg:
        print("Analizando imagen de linea en la ruta: "+linjpeg)
        filenamelin=os.path.basename(linjpeg)
        img=Image.open(linjpeg)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(os.getcwd()+'/'+'Cerrar_Al_Seleccionar_Linea.png')
        image = os.getcwd()+'/'+'Cerrar_Al_Seleccionar_Linea.png'
        linlin=filenamelin.split('_')
        numlin=linlin[4].split('.')[0]
        
        if(os.name=='posix'):
            show=Thread(target=os.system,args=("eog "+image,))
            show.start()
        else:
            show=Thread(target=os.system,args=(image,))
            show.start()
        
        msg2 = "La linea "+str(numlin)+" denota un conteo de Ciclistas en cicloruta, Vehiculos unidireccional o vehiculos bidireccional"   
        choices2 = ["Ciclistas","Peatones","Vehiculos-Uni","Vehiculos-Bidir","Caso Predefinido"]
        seleccion = easygui.buttonbox(msg2, image=image, choices=choices2)
        
        
        """
        **********************VEHICULOS UNIDIRECCIONAL*******************************
        """    
        
        if seleccion == "Vehiculos-Uni":
            msga = "Para la linea #"+ str(numlin)+"\n Indique la informacion correspondiente en las otras ventanas\n cuando termine con las otras ventanas de click en Listo"   
            if parallelo:
                p.append(Thread(target=easygui.buttonbox, args=(msga,), kwargs=dict(image=image, choices=["Listo"])))
                p[-1].start()
            else:
                easygui.buttonbox(msga,image=image, choices=["Listo"])
            
            #Inician preguntas:
            # Es un acceso o una salida
            
            msg = "La linea Afora un Acceso o una Salida a interseccion"   
            choices = ["Acceso","Salida"]
            accOsal = easygui.buttonbox(msg, choices=choices)
            
            if accOsal=="Acceso":
                msg = "Indique el acceso contado con la linea #"+ str(numlin)+"\nA continuacion se le preguntara  el nombre de la Calle, la Carrera y el # del Movimiento"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg, choices=choices)
                Salida=""
                
            elif accOsal=="Salida":
                msg = "Indique la salida contada con la linea #"+ str(numlin)+"\nA continuacion se le preguntara  el nombre de la Calle, la Carrera y el # del Movimiento"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Salida = easygui.buttonbox(msg, choices=choices)
                Acceso=""
            
            
            msg = "Ingrese la informacion para la linea de conteo #"+ str(numlin)
            title = "informacion linea #"+ str(numlin)#;Via_Principal;Via_Secundaria;Movimiento;
            fieldNames = ["Calle","Carrera"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = easygui.multenterbox(msg,title, fieldNames)       
            
            # make sure that none of the fields was left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                  if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" es un campo requerido.\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
                fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            print "Reply was:", fieldValues
            
            if parallelo:
                p[-1].join()
            
            msg = "Describa la linea de conteo de vehiculos?"   
            choices = ["acceso y separador","sentido unico","salida y separador","otro"]
            descripcion_via = easygui.buttonbox(msg,image=image, choices=choices)
            
            
            FILE_report  = open(filereport, 'r') 
            for line in FILE_report:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    # rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),str(fieldValues[2]),Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data1)
                else:
                    print "depurado File_Name"
            """
            **********************CICLISTAS*******************************
            """
        elif seleccion == "Ciclistas":
            """
            msg1 = "Para la linea #"+ str(numlin)+"\n Indique la informacion correspondiente: en las otras ventanas\n"   
            if parallelo:
                p.append(Thread(target=easygui.buttonbox, args=(msg1,), kwargs=dict(image=image, choices=["Listo"])))
                p[-1].start()
                listo="paralelo"
            else:
                listo=easygui.buttonbox(msg1,image=image, choices=["Listo"])
            """
            
            #Inician preguntas:
            # Es un acceso o una salida
            msg2 = "Los ciclistas pasan la linea#"+ str(numlin)+" de izquierda a derecha o de arriba hacia abajo? \nEquivalente a la linea es vertical u horizontal"   
            choices2 = ["Izquierda a Derecha","Arriba a Abajo"]
            accOsal = easygui.buttonbox(msg2,image=image, choices=choices2)
            
            if accOsal=="Izquierda a Derecha":
                msg = "Los ciclistas que vienen de la izquierda de la imagen vienen de que direccion?"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg,image=image, choices=choices)
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
                    
            elif accOsal=="Arriba a Abajo":
                msg = "Los ciclistas c"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg,image=image, choices=choices)
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
            else:
                print("ERROR: saliendo")
                break
            
            
            print ("pasa 3")
            msg = "Ingrese la informacion de ubicacion para la linea de conteo #"+ str(numlin)+ ".\n Use siempre minusculas."
            title = "informacion linea "+ str(numlin)
            fieldNames = ["Calle","Carrera"]
            fieldValues = []
            fieldValues = easygui.multenterbox(msg,title, fieldNames)
            
            # make sure that none of the fields was left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                  if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" es un campo requerido si no sabe ponga -\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
                fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            print "Reply was:", fieldValues
            
            
            print ("pasa 4")
            
            msg = "Describa la linea de conteo de vehiculos?"   
            choices = ["cicloruta","calzada","acera","cicloruta+calzada","cicloruta+acera","calzada+acera","cicloruta+calzada+acera","Ciclovia_Dom_Fest","otro"]
            descripcion_via = easygui.buttonbox(msg,image=image, choices=choices)
            
            if parallelo:
                p[-1].join(15)
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data2)
                else:
                    print "depurado File_Name"
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data3)
                else:
                    print "depurado File_Name"
            FILE_report2.close()
            while show.isAlive():
                Salir = easygui.buttonbox("Por favor cierre la ventana con la imagen de la linea actual", choices=["ok, ya la he cerrado"])
            
            """
            **********************PEATONES*******************************
            """
        elif seleccion == "Peatones":
            """
            msg1 = "Para la linea #"+ str(numlin)+"\n Indique la informacion correspondiente: en las otras ventanas\n"   
            if parallelo:
                p.append(Thread(target=easygui.buttonbox, args=(msg1,), kwargs=dict(image=image, choices=["Listo"])))
                p[-1].start()
                listo="paralelo"
            else:
                listo=easygui.buttonbox(msg1,image=image, choices=["Listo"])
            """
            
            #Inician preguntas:
            # Es un acceso o una salida
            msg2 = "Los peatones pasan la linea#"+ str(numlin)+" de izquiera a derecha o de arriba hacia abajo?"   
            choices2 = ["Izquierda a Derecha","Arriba a Abajo"]
            accOsal = easygui.buttonbox(msg2,image=image, choices=choices2)
            
            if accOsal=="Izquierda a Derecha":
                msg = "Loz peatones que vienen de la izquierda de la imagen vienen de que direccion?"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg,image=image, choices=choices)
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
                    
            elif accOsal=="Arriba a Abajo":
                msg = "Los peatones que vienen de arriba de la imagen vienen de que direccion?"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg,image=image, choices=choices)
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
            else:
                print("ERROR: saliendo")
                break
            
            
            print ("pasa 3")
            msg = "Ingrese la informacion para la linea de conteo #"+ str(numlin)
            title = "informacion linea#"+ str(numlin)#;Via_Principal;Via_Secundaria;Movimiento;
            fieldNames = ["Calle","Carrera"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = easygui.multenterbox(msg,title, fieldNames)       
            
            # make sure that none of the fields was left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                  if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" es un campo requerido si no sabe ponga -\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
                fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            print "Reply was:", fieldValues
            
            
            print ("pasa 4")
            
            msg = "Describa la linea de conteo de peatones:"   
            choices = ["via_peatonal","cicloruta","calzada","acera","cicloruta+calzada","cicloruta+acera","calzada+acera","cicloruta+calzada+acera"]
            descripcion_via = easygui.buttonbox(msg,image=image, choices=choices)
            
            if parallelo:
                p[-1].join(15)
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data2)
                else:
                    print "depurado File_Name"
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data3)
                else:
                    print "depurado File_Name"
            FILE_report2.close()
            while show.isAlive():
                Salir = easygui.buttonbox("Por favor cierre la ventana con la imagen de la linea actual", choices=["ok, ya la he cerrado"])
            
            """
            **********************VEHICULOS BIDIRECCIONAL*******************************
            """  
        elif seleccion == "Vehiculos-Bidir":
            easygui.msgbox("Se va a aforar una linea de conteo bidireccional, tenga presente como se puso la linea de conteo, siempre debe ser de izquierda a derecha o de arriba a abajo. los vehiculos pasaran de manera contraria, si la linea se pone de arriba a abajo, los vehiculos la pasaran de izquierda a derecha.")
            
            """
            msg1 = "Para la linea #"+ str(numlin)+"\n Indique la informacion correspondiente: en las otras ventanas\n"   
            if parallelo:
                p.append(Thread(target=easygui.buttonbox, args=(msg1,), kwargs=dict(image=image, choices=["Listo"])))
                p[-1].start()
                listo="paralelo"
            else:
                listo=easygui.buttonbox(msg1,image=image, choices=["Listo"])
            """
            
            #Inician preguntas:
            # Es un acceso o una salida
            msg2 = "Los vehiculos pasan la linea#"+ str(numlin)+" de izquierda a derecha o de arriba hacia abajo? "   
            choices2 = ["Izquierda a Derecha","Arriba a Abajo"]
            accOsal = easygui.buttonbox(msg2,image=image, choices=choices2)
            
            if accOsal=="Izquierda a Derecha":
                msg = "Loz vehiculos que vienen de la izquierda de la imagen, vienen de que direccion?"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg,image=image, choices=choices)
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
                    
            elif accOsal=="Arriba a Abajo":
                msg = "Los vehiculos que vienen de abajo de la imagen, vienen de que direccion?"   
                choices = ["Norte","Sur","Oriente","Occidente"]
                Acceso = easygui.buttonbox(msg,image=image, choices=choices)
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
            else:
                print("ERROR: saliendo")
                break
            
            
            print ("pasa 3")
            msg = "Ingrese la informacion para la linea de conteo #"+ str(numlin)+"\n Si la linea esta sobre la cicloruta, haga Movimiento = Ciclistas cicloruta\n  si esta sobre la via, haga Movimiento =  Ciclistas Via"
            title = "informacion linea#"+ str(numlin)#;Via_Principal;Via_Secundaria;Movimiento;
            fieldNames = ["Calle","Carrera"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = easygui.multenterbox(msg,title, fieldNames)       
            
            # make sure that none of the fields was left blank
            while 1:
                if fieldValues == None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                  if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" es un campo requerido si no sabe ponga -\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
                fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            print "Reply was:", fieldValues
            
            
            print ("pasa 4")
            
            msg = "Describa la linea de conteo de vehiculos?"   
            choices = ["acceso salida y separador","doble via","otro"]
            descripcion_via = easygui.buttonbox(msg,image=image, choices=choices)
            
            if parallelo:
                p[-1].join(15)
                
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data2)
                else:
                    print "depurado File_Name"
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data3)
                else:
                    print "depurado File_Name"
            FILE_report2.close()
            
            while show.isAlive():
                Salir = easygui.buttonbox("Por favor cierre la ventana con la imagen de la linea actual", choices=["ok, ya la he cerrado"])
            
            
            
            
            """
            **********************    CASO PREDEFINIDO   *******************************
            """  
        elif seleccion == "Caso Predefinido":
            msg = "Que caso es:"   
            choices = ["CL17X115-E-W","Peatonal AK7 AC12","cicloruta AK11 AC100","cicloruta+calzada AK11 AC100","cicloruta AK19 AC100"]
            casoparticular = easygui.buttonbox(msg,image=image, choices=choices)  
            
            if casoparticular=="Peatonal AK7 AC12":
                Acceso="Norte"
                Salida="Sur"
                fieldValues=['12', '7']
                descripcion_via="via_peatonal"
                
            elif casoparticular=="cicloruta AK11 AC100":
                Acceso="Norte"
                Salida="Sur"
                fieldValues=['100', '11']
                descripcion_via="cicloruta"
            
            elif casoparticular=="cicloruta+calzada AK11 AC100":
                Acceso="Norte"
                Salida="Sur"
                fieldValues=['100', '11']
                descripcion_via="cicloruta+calzada"
            
            elif casoparticular=="cicloruta AK19 AC100":
                Acceso="Norte"
                Salida="Sur"
                fieldValues=['100', '19']
                descripcion_via="cicloruta"
            elif casoparticular=="CL17X115-E-W":
                Acceso="Oriente"
                Salida="Occidente"
                fieldValues=['17', '115']
                descripcion_via="cicloruta"
                
                
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data2)
                else:
                    print "depurado File_Name"
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(folder,lindata[0],numlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    rp.agregarData(Data3)
                else:
                    print "depurado File_Name"
            FILE_report2.close()
            while show.isAlive():
                Salir = easygui.buttonbox("Por favor cierre la ventana con la imagen de la linea actual", choices=["ok, ya la he cerrado"])
                    
        
rp.cerrarArchivo()
os.system("tail -n+2 "+folder+"/reporte_general_carpeta.csv > "+folder+"/reporte_general_carpeta_sinmarco.csv")

#ahora toca unir todos los .csv de la linea en un solo archivo. 
        

#exit()
