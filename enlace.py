 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time
import desempacotar

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

import empacotador

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data_to_send, txLen):
        """ Send data over the enlace interface
        """
        #Tipo 1: Abre pede comunicação para o server
        startTime = time.time()
        dados = []
        tipo2_recebido = False
        waiting_ack = False
        error_count = 0
        while(time.time() - startTime < 5):
            self.tx.sendBuffer(empacotador.empacotar([],1,0))
            dados = self.rx.getBuffer(self.rx.getBufferLen())
            time.sleep(0.2)
            if(len(dados) < 23):
                continue
            else:
                print(len(dados))
                isOk, payload, msgType = desempacotar.depack(dados,len(dados))
                if(isOk):
                    if(msgType == 2):
                        tipo2_recebido = True
                        dados = []
                        startTime = time.time()
                        dados = self.rx.getBuffer(self.rx.getBufferLen())
                        self.tx.sendBuffer(empacotador.empacotar([],3,0))
                        waiting_ack = True
                    if(tipo2_recebido and (not waiting_ack)):
                        self.tx.sendBuffer(empacotador.empacotar(data_to_send,4,txLen))
                        waiting_ack = True
                    if(waiting_ack and (msgType == 6)):
                        self.tx.sendBuffer(empacotador.empacotar(data_to_send,4,txLen))
                        startTime = time.time()
                        print("Received NACK, resending data for the {} time".format(error_count+1))
                        error_count += 1
                    elif(msgType == 5):
                        break
                    if(error_count > 5):
                        print("Too much atempts, shutting down")
                        break
                else:
                    print("Error at ENLACE: Could not depack data. Stopping transmission")
                    break               
                    

        else:
            #Timeout Error
            print("TIMEOUT_ERROR:", end=" ")
            if(not tipo2_recebido):
                print("No response from server")
        packedData = empacotador.empacotar(data_to_send,4, txLen)


    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler em algum momento' )

        data = self.rx.getNData()
        msg_type, data_valid , data_parsed = desempacotar.depack(data,len(data))
       
        return(data_parsed, len(data_parsed))





