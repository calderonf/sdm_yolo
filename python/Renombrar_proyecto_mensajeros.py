#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 07:27:00 2020

@author: Francisco Calderon
"""

#1******************************************************************************************************************************OK
import os
import time
import subprocess
import numpy as np
import datetime
import shutil

from tkinter import filedialog
from tkinter import *


from Secretos.listadoRappis import esRappi

#2******************************************************************************************************************************OK
def get_path():

    """
    open a GUI to select folder

    Parameters
    ----------
    No input arguments

    Returns
    -------
        return string of a folder chosen by user, function returns None for no selection

    """

    root = Tk()
    root.withdraw()

    # Open GUI to select folder
    folder_selected = filedialog.askdirectory(initialdir="/Users/francisco/Dropbox/RAPPISCUARENTENA/", title = "Seleccione Una Carpeta")

    # Return user selection
    if folder_selected == "":
        return None
    else:
        return folder_selected 
    

#3******************************************************************************************************************************OK
def create_folders(folder):
    """
    crea carpetas necesaria para guardar el resultado

    Parameters
    ----------
    No input arguments

    Returns
    -------
        return string of a folder chosen by user, function returns None for no selection

    """
    # para entrenar mensajeros. 
    
    if not os.path.exists(folder+"/"+"/LOGO_RAPPI_EN_LISTA"):
        os.mkdir(folder+"/"+"/LOGO_RAPPI_EN_LISTA")
        
    if not os.path.exists(folder+"/"+"/LOGO_RAPPI_NO_LISTA"):
        os.mkdir(folder+"/"+"/LOGO_RAPPI_NO_LISTA")
    
    
#4******************************************************************************************************************************OK
def get_list(path):
    dirlist=os.listdir(path)
    dirlist.sort()
    listasal=[]
    for image_file in dirlist:

        # take only file with .MP4 extension
        # This form already return file by file in name order 
        if image_file.endswith("JPG"):
            listasal.append(image_file)
    return listasal
#4******************************************************************************************************************************OK
def organize(path,list_files):
    for imfile in list_files:
        placa=imfile.split("-")[0]
        if esRappi(placa):
            shutil.move(path+"/"+imfile,path+"/"+"/LOGO_RAPPI_EN_LISTA/"+imfile)
        else:
            shutil.move(path+"/"+imfile,path+"/"+"/LOGO_RAPPI_NO_LISTA/"+imfile)
            
    
    
    
    
def create_folders(folder):
    """
    crea carpetas necesaria para guardar el resultado

    Parameters
    ----------
    No input arguments

    Returns
    -------
        return string of a folder chosen by user, function returns None for no selection

    """
    # para entrenar mensajeros. 
    
    if not os.path.exists(folder+"/"+"/LOGO_RAPPI_EN_LISTA"):
        os.mkdir(folder+"/"+"/LOGO_RAPPI_EN_LISTA")
        
    if not os.path.exists(folder+"/"+"/LOGO_RAPPI_NO_LISTA"):
        os.mkdir(folder+"/"+"/LOGO_RAPPI_NO_LISTA")
    
if __name__ == '__main__':
    # Set a timer to count the total process time
    process_time_start = time.time() 

    # Open a GUI to select folder
    folder= get_path()
    
    # Create folders to store results
    create_folders(folder)
    
    # traer lista de archivos
    archivos=get_list(folder)
    
    #ordenar archivos rappis
    organize(folder,archivos)

    # Print and report the Total process time
    print("\nTotal process time -", time.strftime('%H:%M:%S',time.gmtime(int(time.time() - process_time_start))))
    
    # Wait for user confirmation
    input("Press Enter to continue...")
#******************************************************************************************************************************


   
