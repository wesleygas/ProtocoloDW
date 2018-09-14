def depack(data,len_data):
    head_size = 20
    data_list = list(data)
    if (len(data_list)<21):
        return None, False, None, None, None, None
    head = data_list[:head_size]
    # print(data_list)


    size = int(head[0])
    
    # size = 
    package_number = int.from_bytes(head[1:3], byteorder = 'big')
    package_total = int.from_bytes(head[3:5], byteorder = 'big')
    msg_type = int(head[5])


    if msg_type == 8:
        package_expected = int.from_bytes(head[6:8], byteorder = 'big')
    else:
        package_expected = None

    print("--------------------------------")
    print("A mensagem é do tipo {0}".format(msg_type))
    # print("Overhead:" , (size/len_data))


    found_eop,list_unpacked = find_EOP(len_data,data_list,head_size)
	# print(size)
    if (len(list_unpacked) == size and found_eop == True):

    	return msg_type, True, bytes(list_unpacked), package_number, package_total, package_expected
    elif (found_eop == False):
    	print("EOP não encontrado")
    	return msg_type, False, bytes(list_unpacked), package_number, package_total, package_expected
    elif (len(list_unpacked) != size):
    	print("Tamanho no HEAD não são compativeis com os dados recebidos")
    	print("Deveria ser {0} bytes e foram {1}".format(len(list_unpacked),  size))
    	return msg_type, False, bytes(list_unpacked), package_number, package_total, package_expected
    else:
    	return msg_type, False, bytes(list_unpacked), package_number, package_total, package_expected



    return msg_type, False, bytes(list_unpacked), package_number, package_total, package_expected

def find_EOP(len_data, data_list,head_size):
    list_unpacked = []
    found_eop = False
    i = head_size
    stuffed_payload = [190,239,186,239,218,239]
    while i < len_data:
        # print("OK")
        if data_list[i:i+6] == stuffed_payload:
            list_unpacked += [190,186,218]
            i += 6
        elif data_list[i:i+3] == [190,186,218]:
            found_eop = True
            print("EOP encontrado na posição {0} do pacote".format(i-20))
            break
        else:
            list_unpacked.append(data_list[i])
            i += 1


    return found_eop, list_unpacked


def find_EOP_BUFFER(len_data, data):
    data_list = list(data)
    found_eop = False
    i = 0
    for i in range(len_data -2):
        #print("OK")
        if data_list[i:i+3] == [190,186,218]:
            found_eop = True

            print("EOP encontrado na posição {0} do buffer".format(i+1))
            return found_eop, i



    return found_eop, i







