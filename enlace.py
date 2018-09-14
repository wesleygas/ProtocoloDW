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
        package_list = empacotador.empacotar(data_to_send,4,txLen)
        print("Starting transmission of {} packages in total of {} bytes of data".format(len(package_list),txLen))
        startTime = time.time()
        data_type = 1
        msgType = 0
        dados = []
        #waiting_ack = False
        error_count = 0
        tipo2_recebido = False
        txIsUp = True
        while(time.time() - startTime < 20):
            if(data_type == 1):
                print("Mandando tipo 1")
                self.tx.sendBuffer(empacotador.empacotar(0,1,0)[0])
                responseTime = time.time()
                while(time.time() - responseTime < 1.5):
                    dados = self.rx.getNData()
                    msgType, isOk, data, rxPack_number, rxPack_total, rxPack_expected = desempacotar.depack(dados,len(dados))
                    print("RECEBI MSG DO TIPO",msgType)
                    if(msgType == 2):
                        data_type = 2
                        startTime = time.time()
                        tipo2_recebido = True
                        break
            elif(data_type == 2):
                print("Mandando tipo 3")
                time.sleep(1)
                self.rx.clearBuffer()
                self.tx.sendBuffer(empacotador.empacotar(0,3,0)[0])
                responseTime = time.time()
                while(time.time() - responseTime < 3):
                    dados = self.rx.getNData()
                    msgType, isOk, data, rxPack_number, rxPack_total, rxPack_expected = desempacotar.depack(dados,len(dados))
                    if(msgType == 2):
                        self.tx.sendBuffer(empacotador.empacotar([],3,0)[0])
                        print(" ----- Reenviando tipo 3")
                else:
                    data_type = 4
            elif(data_type == 4):
                package_number = 0
                while package_number < len(package_list) and txIsUp:
                    package = package_list[package_number]
                    self.tx.sendBuffer(package)
                    while(time.time() - responseTime < 10):
                        dados = self.rx.getNData()
                        msgType, isOk, data, rxPack_number, rxPack_total, rxPack_expected = desempacotar.depack(dados,len(dados))
                        if(isOk):
                            if(msgType == 5):
                                print("Received ACK for package", package_number)
                                responseTime = time.time()
                                package_number += 1
                                msgType = 4
                                break
                            elif(msgType == 6):
                                print("Received NACK, resending package {0} for the {1} time".format(package_number,error_count+1))
                                responseTime = time.time()
                                error_count += 1 
                                msgType = 4                           
                                break
                            elif(msgType == 8):
                                package_number = rxPack_expected
                                msgType = 4
                                break
                            if(msgType == 7):
                                print("Received \"Tchau\", stopping transmission now.")
                                txIsUp = False
                                break
                        if(error_count > 5):
                            print("Too many atempts, shutting down")
                            self.tx.sendBuffer(empacotador.empacotar([],7,0)[0])
                            txIsUp = False
                            break 
                else:
                    if(txIsUp):
                        print("Transmission succeded! Eh hora de dar Tchau!") 
                        self.tx.sendBuffer(empacotador.empacotar([],7,0)[0])
                        break
                    else:
                        print("Timeout, stopping transmission.")
                        self.tx.sendBuffer(empacotador.empacotar([],7,0)[0])
                        break

                    
        else:
            #Timeout Error
            print("TIMEOUT_ERROR:", end=" ")
            if(not tipo2_recebido):
                print("No response from server")
        


    def getData(self, size):
        info_util = b""


        self.rx.clearBuffer()
        msg_types_valid = [1,3,4,7]
        msg_types_received =[]
        # contagem de pacotes
        packages_received = -1
        bytes_received = b""

        print('entrou na leitura e tentara ler em algum momento' )
        while(True):
            self.rx.clearBuffer()
            data = self.rx.getNData()
            msg_type, data_valid , data_parsed , package_number, package_total, package_expected = desempacotar.depack(data,len(data))


            if (data_valid == False or msg_type != 1):
                continue


            elif (msg_type in msg_types_valid):  #Começa a visualizar os outros pacotes
                startTime = time.time()
                msg_types_received = []


                while(time.time()-startTime<15):

                    data = self.rx.getNData()
                    msg_type, data_valid, data_parsed, package_number, package_total, package_expected = desempacotar.depack(data,len(data))
                    

                    if msg_type == 1:
                        self.rx.clearBuffer()
                        msg_types_received = [1]
                        startTime = time.time()
   
                   
                    elif (msg_type in msg_types_valid):
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
                            self.tx.sendBuffer(empacotador.empacotar(0,2,0)[0])
                        
                        elif (msg_types_received == [1,3]):
                            self.rx.clearBuffer()
                            pass

                        elif (msg_types_received == [1,3,4]):
                            

                            if data_valid:

                                if package_number == (packages_received + 1):
                                    pacote_enviado = empacotador.empacotar(0,5,0)[0]
                                    # print(pacote_enviado)
                                    self.tx.sendBuffer(pacote_enviado)
                                    print("Recebi o pacote correto, pacote {0} de {1}".format(package_number, package_total) )
                                    bytes_received += data_parsed
                                    packages_received = package_number


                                    if package_number == package_total:
                                        self.tx.sendBuffer(empacotador.empacotar(0,7,0)[0])
                                        return (bytes_received, len(bytes_received))


                                else:
                                    pacote_erro = empacotador.empacotar((packages_received+1),8,0)[0]
                                    # print(pacote_erro)
                                    self.tx.sendBuffer(pacote_erro)
                                    print("Não recebi o pacote correto, deveria ser {0} e é {1}".format(packages_received + 1, package_number) )
                                
                            else:
                                self.tx.sendBuffer(empacotador.empacotar(0,6,0)[0])

                        elif(msg_types_received == [1,3,4,7]):
                            return (bytes_received, len(bytes_received))

                        if (msg_type == 7):
                            return(b"", 0)

                else:
                    print("TIMEOUT_ERROR NO RECEIVE")
                    return(b"", 0)

            else:
                print("Ordens de mensagens não correta")
                continue


        return(data_parsed, len(data_parsed))





