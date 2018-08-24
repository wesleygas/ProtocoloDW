def depack(data,len_data):
    head_size = 20
    data_list = list(data)
    head = data_list[:head_size]
    list_unpacked = []
    # print(data_list)
    size = int.from_bytes(head[0:2], byteorder = 'big')
    # print ("Tamanho esperado: ", size)
    found_eop = False
    i = head_size
    while i < len_data:
        # print("OK")
        stuffed_payload = [190,239,186,239,218,239]
        if data_list[i:i+6] == stuffed_payload:
            list_unpacked += [190,186,218]
            i += 6
        elif data_list[i:i+3] == [190,186,218]:
        	found_eop = True
        	print("EOP encontrado na posição {0}".format(i-20))
        	break
        else:
            list_unpacked.append(data_list[i])
            i += 1

    print("Overhead:" , (size/len_data))
	# print(size)
    if (len(list_unpacked) == size and found_eop == True):

    	return True, bytes(list_unpacked)
    elif (found_eop == False):
    	print("EOP não encontrado")
    	return False, bytes(list_unpacked)
    elif (len(list_unpacked) != size):
    	print("Tamanho no HEAD não são compativeis com os dados recebidos")
    	print("Deveria ser {0} bytes e foram {1}".format(list_unpacked,size))
    	return False, bytes(list_unpacked)
    else:
    	return False, bytes(list_unpacked)










