maxPayloadLen = 65535
EOP = int("0xBEBADA", 16)

def empacotar(data, size):
    global maxPayloadLen, EOP
    packedData = []
    dataList = list(data)
    payloads = slicer(dataList, size)
    #TODO: Stuff this shit!
    
    print(len(payloads[0]))
    for i in range(len(payloads)):
        head = [0]*20
        payloadSize = (len(payloads[i])).to_bytes(2, byteorder='big')
        head[0:2] = payloadSize
        head[2] = i
        head[3] = len(payloads)
        head = bytes(head)
        stuffed_payload = stuff(payloads[i])

        packedData += list(head) + stuffed_payload + list(EOP.to_bytes(3, byteorder='big'))



    
    return bytes(packedData)


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


def stuff(data):
    stuffed_payload = []       
    
    return stuffed_payload