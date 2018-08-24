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
from tkinter.filedialog import askopenfilename, asksaveasfile

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem145231" # Mac    (variacao de)
# serialName = "COM20"                  # Windows(variacao de)
baurdrate = 115200


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")


    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("gerando dados para transmissao :")
    
    Tk().withdraw()
    filename = askopenfilename()
    #extension = "." + filename.split(".")[-1]
    with open(filename, "rb") as File:
         f = File.read()
         b = bytearray(f)

    print("Peguei o arquivo" + filename)
   



    txLen    = len(b)
    # print(txLen)
    ETTransmit = 2*txLen/(baurdrate/8)
    print("Tempo estimado para a transferencia: {} segundos".format(ETTransmit)) 
    throughput = txLen/ETTransmit
    print("Throughput: ", throughput)
    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))

    
    
    startTime = time.time()
    com.sendData(b, txLen)
    
    txSize = com.tx.getStatus()
    # print (txSize)
    print("Transferência finalizada em {} segundos".format((time.time() - startTime)))
    



        
    # Atualiza dados da transmissão
    
   

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    startTime = time.time()
    main()