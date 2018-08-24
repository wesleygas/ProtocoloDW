def depack(data,len_data):
	head_size = 20
	data_list = list(data)
	head = data_list[:head_size+1]
	print("ok")
	size = int.from_bytes(head[0:2], byteorder = 'big')
	print ("Tamanho esperado: ", size)
	for i in range (head_size,len_data):
		lista_end = [190,186,218]
		if data[i:i+3] == [190,186,218]:
			print("Inicio do end of package",i)
			if (i == len_data-3):
				return bytes(data_list[20:i]), True

			else:
				return bytes(data_list), False

