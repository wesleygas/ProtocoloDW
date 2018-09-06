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
        data_type = 1
        dados = []
        waiting_ack = False
        error_count = 0
        tipo2_recebido = False
        while(time.time() - startTime < 5):
            if(data_type == 1):
                self.tx.sendBuffer(empacotador.empacotar([],1,0))
                print("Mandando tipo 1")
                dados = self.rx.getNData()
                msgType, isOk, data = desempacotar.depack(dados,len(dados))
                print("RECEBI MSG DO TIPO",msgType)
                if(msgType == 2):
                    data_type = 2
                    tipo2_recebido = True
            elif(data_type == 2):
                self.tx.sendBuffer(empacotador.empacotar([],3,0))
                print("Mandando tipo 3")
                data_type = 4
            elif(data_type == 4):         
                print("Sending actual Data")
                self.tx.sendBuffer(empacotador.empacotar(data_to_send,4,txLen))
                waiting_ack = True
                dados = self.rx.getNData()
                msgType, isOk, data = desempacotar.depack(dados,len(dados))

            if(waiting_ack and (msgType == 6)):
                self.tx.sendBuffer(empacotador.empacotar(data_to_send,4,txLen))
                startTime = time.time()
                print("Received NACK, resending data for the {} time".format(error_count+1))
                error_count += 1

            elif(msgType == 5):
                print("Received ACK, stopping transmission")
                self.tx.sendBuffer(empacotador.empacotar(data_to_send,7,txLen))
                break
            
            if(msgType == 7):
                print("Received stop msg, stopping transmission now.")
                break
            if(error_count > 5):
                print("Too many atempts, shutting down")
                break  
                    
        else:
            #Timeout Error
            print("TIMEOUT_ERROR:", end=" ")
            if(not tipo2_recebido):
                print("No response from server")
        


    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """

        info_util = b""


        self.rx.clearBuffer()
        msg_types_valid = [1,3,4,7]
        msg_types_received =[]
        print('entrou na leitura e tentara ler em algum momento' )
        while(True):
            self.rx.clearBuffer()
            data = self.rx.getNData()
            msg_type, data_valid , data_parsed = desempacotar.depack(data,len(data))


            if (data_valid == False or msg_type != 1):
                continue


            elif (msg_type in msg_types_valid):  #Começa a visualizar os outros pacotes
                startTime = time.time()
                msg_types_received = []


                while(time.time()-startTime<15):

                    data = self.rx.getNData()
                    msg_type, data_valid , data_parsed = desempacotar.depack(data,len(data))
                    

                    if msg_type == 1:
                        self.rx.clearBuffer()
                        msg_types_received = [1]
                        startTime = time.time()
   
                   
                    elif (msg_type in msg_types_valid):
                        # print("recebi isso aqui", msg_type)
                        if (msg_type not in msg_types_received):
                            startTime = time.time()
                            if msg_type == msg_types_valid[len(msg_types_received)]:
                                msg_types_received.append(msg_type)
                                
                            else:
                                print("Ordem de mensagem errada")
                        else:
                            startTime = time.time()
                    else:
                        print("recebi essa mensagem do tipo",msg_type)
                        pass

                    print(msg_types_received)

                    if msg_type != None:

                        if (msg_types_received == [1]):
                            # print("mandei o tipo 2")
                            # self.rx.clearBuffer()
                            self.tx.sendBuffer(empacotador.empacotar([],2,0))
                        
                        elif (msg_types_received == [1,3]):
                            # print("hurray")
                            pass

                        elif (msg_types_received == [1,3,4]):
                            # print(msg_types_received)
                            pass

                            if data_valid:
                                self.tx.sendBuffer(empacotador.empacotar([],5,0))
                                # print("mandei o tipo 5")
                                info_util = data_parsed

                                
                            else:
                                self.tx.sendBuffer(empacotador.empacotar([],6,0))
                                # print("mandei o tipo 6")

                        elif(msg_types_received == [1,3,4,7]):
                            return (info_util, len(info_util))

                        if (msg_type == 7):
                            return(b"", 0)

                else:
                    print("TIMEOUT_ERROR NO RECEIVE")
                    return(b"", 0)

            else:
                print("Ordens de mensagens não correta")
                continue


        return(data_parsed, len(data_parsed))





