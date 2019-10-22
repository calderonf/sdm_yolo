# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:58:32 2019

@author: francisco
"""

import subprocess
#top -b -n 1 -u francisco
res = subprocess.check_output(["top","-b","-n 1","-u","francisco"])
#  PID USUARIO   PR  NI    VIRT    RES    SHR S  %CPU %MEM     HORA+ ORDEN
PID=0
CPU=8
MEMORIA=9
ORDEN=11

first=True
for line in res.splitlines():
    if first:
        print(line)
        first=False
        continue
    lined=line.decode(encoding="utf8")
    lined=lined.replace("     ", "&")
    lined=lined.replace("    ", "&")
    lined=lined.replace("   ", "&")
    lined=lined.replace("  ", "&")
    lined=lined.replace(" ", "&")
    lined=lined.replace("\t", "&")
    lined=lined.replace("\n", "&")
    linesplit=lined.split("&")
    if(linesplit[0]==""):
        linesplit.pop(0)
    #print (linesplit)
    
    if len (linesplit)==ORDEN+1:
        #print ("entra")
        if linesplit[ORDEN]=="python2":
            print(lined)
            print(linesplit)
            print("process: ",linesplit[ORDEN])
            # si el proceso de python no esta usando por lo menos un 50% de la CPU matelo
            cpu_use=float(linesplit[CPU].replace(",","."))
            pid=str(linesplit[PID])
            print ("%CPU= ", cpu_use)
            if (cpu_use<10):
                res2 = subprocess.check_output(["kill",linesplit[PID]])
                print("se mata el proceso",linesplit[PID] )
