

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

print("comecou")

from enlace import *

import time

from tkinter import Tk
from tkinter.filedialog import asksaveasfile


# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem144241" # Mac    (variacao de)
# serialName = "COM14"                  # Windows(variacao de)

mockData = False

print("porta COM aberta com sucesso")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")

        
    # Atualiza dados da transmissão

   

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    bytesSeremLidos=com.rx.getBufferLen()
  
        
    rxBuffer, nRx = com.getData(20)

    # log
    print ("Lido              {} bytes ".format(nRx))
 
    # with open("gatineo.jpg", "wb+") as image:
    #     f = image.write(rxBuffer)
    # print (rxBuffer)

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()
    # defaultextension = ".jpg"
    if(not mockData):
        Tk().withdraw()
        f = asksaveasfile(mode='wb')
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            pass
        else:
            f.write(rxBuffer)
            f.close() # `()` was missing.
    else:
        print(rxBuffer)
   #print (rxBuffer)

    



    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
