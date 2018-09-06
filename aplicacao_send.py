#!/usr/bin/env python3
# -*- coding: utf-8 -*-


print("comecou")

from enlace import * 
import time

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile


#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports


#serialName = "/dev/cu.usbmodem145231" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)
baurdrate = 115200
mockFile = True #Se quiser só mandar x dados ao invés de escollher um arquivo toda vez


def telemetry(txLen, baurdrate):
    ETTransmit = 2*txLen/(baurdrate/8)
    print("Tempo estimado para a transferencia: {} segundos".format(ETTransmit)) 
    throughput = txLen/ETTransmit
    print("Throughput: ", throughput)

def main():
    global telemetry
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()
    rawData = []
    print("comunicação aberta")
    print ("gerando dados para transmissao :")
    if(mockFile):
        for i in range(200):
           rawData.append(i)
        rawData = bytes(rawData)
    else:
        Tk().withdraw() #Disable main TK window
        filename = askopenfilename() #Ask for file 
        #extension = "." + filename.split(".")[-1]
        with open(filename, "rb") as File:
            f = File.read()
            rawData = bytearray(f)
        print("Peguei o arquivo" + filename)


    txLen = len(rawData)
    #Print Telemetry Data
    telemetry(txLen, baurdrate)
    
    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))

    
    
    startTime = time.time()
    com.sendData(rawData, txLen)
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
