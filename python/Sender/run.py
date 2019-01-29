import os
import subprocess
        

class exeCommand:
    
    def __init__(self, ipremota,puertoremoto,usuarioremoto):
        """
        Inicializacion\n
        Clase exeCommand \n
        ejecuta un comando y retorna exito o fallo \n
    
        los metodos son: \n
            __init__ \n
            enviarClavePublica \n
            ejecutarComandoPCRemoto \n
            
        \n
        USO:\n
        \n
        inicializar con direccion ip del servidor donde se estan ejecutando los comandos remotos\n
            
        
        
        
        LLAMADO:\n
        
        
            \n
        EJEMPLOS:\n
         
        """
        self.ipremota=ipremota
        self.puertoremoto=puertoremoto
        self.usuarioremoto=usuarioremoto
        p = subprocess.Popen("whoami", stdout=subprocess.PIPE)
        if not p.returncode:
            self.localuser=p.communicate()[0].rstrip()
            self.remoteshell="ssh"
            self.remotecopy="scp"
            self.rutallave="/home/"+self.localuser+"/.ssh/"
            self.login=self.usuarioremoto+"@"+self.ipremota
        else:
            print ("ERROR: error al solicitar nombre de usuario en PC local")
      
    def enviarClavePublica(self):
        """
        Tomado de 
        http://www.linuxproblem.org/art_9.html
        cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
        """
        runcmd="cat "+self.rutallave+"id_rsa.pub | ssh "+self.usuarioremoto+"@"+self.ipremota+" 'cat >> .ssh/authorized_keys'"
        print ("Por Favor ejecute en una terminal el siguiente comando para enviar su llave publica y que no solicite contrasena")
        print (runcmd)
        print ("Finalizado esto ejecute:")
        print (self.remoteshell+" "+self.login)
        print ("y verifique que no se le pida contrasena para acceder al PC remoto")

    def ejecutarComandoPCRemoto(self, comando):
        """
        Ejecuta un comando en un PC remoto usando ssh y la configuracion de la clase, por favor verifique que se cumple con los pasos en 
        el metodo enviarClavePublica()
        """
        print ("ejecutando comando "+self.login+comando)
        
        
        p = subprocess.Popen([self.remoteshell,self.login,comando], stdout=subprocess.PIPE)
        if not p.returncode:
            print ("comando exitoso retorna")
            print (p.communicate())
        else:
            print ("ERROR: no se pudo ejecutar comando en PC remoto revise conectividad, puertos y acceso por llave publica con enviarClavePublica()")


    def enviarArchivo(self, archivo_a_enviar,ruta_destino):
        """
        Envia un archivo de una ruta especifica a un destino en el PC configurado en la clase
        scp /home/user/table.csv jane@ordenador.ejemplo.com:/home/jane/
        """
        
        p = subprocess.Popen([self.remotecopy,archivo_a_enviar,self.login+":"+ruta_destino], stdout=subprocess.PIPE)
        if not p.returncode:
            print ("comando exitoso retorna")
            print (p.communicate())
        else:
            print ("ERROR: no se pudo ejecutar comando en PC remoto revise conectividad, puertos y acceso por llave publica con enviarClavePublica()")
        
        
        
        

if __name__ == "__main__":
   
    
    ejecute=exeCommand("192.168.1.174","22","francisco")
    ejecute.enviarClavePublica()
    ejecute.ejecutarComandoPCRemoto("fortune")
    
    
    
    
    
    
    
    
    
    
    