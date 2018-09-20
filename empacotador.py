from crc import crc16
maxPayloadLen = 128
EOP = int("0xBEBADA", 16)

#Quando data_type=4, recebe um byte-array e retorna uma lista com byte arrays
#de tamanho máximo "maxPayloadLen" [(bytearray,(bytearray),...]
#Quando data_type=8, recebe o número do pacote em (data)
#no mais, apenas retorna um pacote nulo do tipo especificado [(bytearray)]
def empacotar(data, data_type, size):
    global maxPayloadLen, EOP
    packedData_List = []
    end_of_package = list(EOP.to_bytes(3, byteorder='big'))  
    if(data_type == 4):
        dataList = list(data)
        payloads = slicer(dataList, size)
        #TODO: Stuff this shit!
        
        #print(len(payloads[0]))
        for i in range(len(payloads)):
            head = [0]*20
            head[0] = len(payloads[i])
            packageNumber = (i).to_bytes(2, byteorder='big')
            head[1:3] = packageNumber
            head[3:5] = (len(payloads)).to_bytes(2, byteorder='big')
            head[5] = data_type
            head[8:12] =  int(crc16(payloads[i])).to_bytes(4, byteorder='big')
            stuffed_payload = stuff(payloads[i])
            packedData_List.append(bytes(head + stuffed_payload + end_of_package))
    
    elif(data_type == 8):
        head = [0]*20
        head[5] = data_type
        head[6:8] = list(data.to_bytes(2, byteorder='big'))
        packedData = head + end_of_package
        packedData_List.append(bytes(packedData))
    
    else:
        head = [0]*20
        head[5] = data_type
        packedData = head + end_of_package
        packedData_List.append(bytes(packedData))

    
    return packedData_List

#Recebe uma lista com n elementos e divide em listas de tamanho maximo=size
def slicer(data, size):
    global maxPayloadLen
    dataCache = list(data)
    payloads = []
    if(size <= maxPayloadLen):
        payloads.append(data)

    else:
        for i in range(0, size, maxPayloadLen):
            payloads.append(dataCache[i:i+maxPayloadLen])

    return payloads

#Faz o stuffing do EOP
def stuff(data):
    stuffed_payload = []       
    i = 0
    while(i < len(data)):
        if(data[i:i+3] == [190,186,218]):
            print("Found EOP within data at position ",i)
            stuffed_payload+= [190,239,186,239,218,239]
            i+= 3
        else:
            stuffed_payload.append(data[i])
            i+= 1

    return stuffed_payload