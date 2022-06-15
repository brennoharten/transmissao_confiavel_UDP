import socket, os, sys, functions

port = 5000
host = '127.0.0.1'
pack_size=150
server_size=66		#pacote = 16 porta origem + 16 porta destino + 16 comp + 1 ack + 1 seq + 16 checksum
recivedData=[]
recivedDataOrder=[]
duplicatedDatas=[]
corruptedDatas=[]
data=0
i=0

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host,port))

filename, addr = server.recvfrom(1024)
filesize, addr = server.recvfrom(1024)
filename = os.path.basename(filename)
filesize = int(filesize)

oncethru=0

while 1:
	
	with open(filename, 'wb',filesize) as f:
		for rc in recivedDataOrder:
			str_val = str(rc) 
			byte_val = str_val.encode() 
			f.write(byte_val)
	#Estado 0

	d = server.recvfrom(pack_size)
	data = d[0]
	addr = d[1]

	if not data: 
		break

	i+=1
	os.system('clear')
	

	#Extraindo datas do pacote
	originDoor=int(data[0:16],2)
	endDoor=int(data[16:32],2)
	comp=int(data[32:48],2)
	checksum=int(data[48:64],2)
	seq = int(data[64:65],2)
	data=int(data[65:97],2)
	lastData=data

	sum = functions.checksum(originDoor,endDoor,comp)
	
	if (seq==1):
		print("\nPacote ["+str(lastData)+"] duplicado! Descartando e re-solicitando...")
		duplicatedDatas.append(lastData)
	if (sum!=checksum):
		print("\nPacote ["+str(data)+"] com erro de bits! Descartando e re-solicitando...")
		corruptedDatas.append(data)
	while (seq==1 or sum!=checksum):
		if (oncethru==1):
			try :
				#Enviando mensagem ao cliente informando pacote duplicado/corrompido
				server.sendto(msg.encode("ascii"), addr)
			except socket.error as msg:
				print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
				sys.exit()

		
		# Recebendo datas do cliente (datas, endereço)
		d = server.recvfrom(pack_size)
		data = d[0]
		addr = d[1]
		if not data: 
			break

		#Extraindo datas do pacote
		originDoor=int(data[0:16],2)
		endDoor=int(data[16:32],2)
		comp=int(data[32:48],2)
		checksum=int(data[48:64],2)
		seq = int(data[64:65],2)
		lastData=data
		data=int(data[65:97],2)

		sum = functions.checksum(originDoor,endDoor,comp)

	if (seq==0 and sum==checksum):
		recivedData.append(data)
		recivedDataOrder.append(str(data) + "\n")
		recivedDataOrder.sort()
		print("\nPacote ["+str(data)+"] recebido corretamente!")
		print("\nPacotes recebidos até o momento:")
		print(recivedData)
		print("\nPacotes duplicados:")
		print(duplicatedDatas)
		print("\nPacotes corrompidos:")
		print(corruptedDatas)
		msg = functions.creat_pack_server(server.getsockname()[1],port,server_size,1,0)
        

		try :
			#Enviando mensagem ao cliente
			server.sendto(msg.encode("ascii"), addr)
		except socket.error as msg:
			print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
			sys.exit()
		oncethru=1


	#Estado 1
	# Recebendo datas do cliente (datas, endereço)
	d = server.recvfrom(pack_size)
	data = d[0]
	addr = d[1]

	if not data: 
		break

	#Extraindo datas do pacote
	originDoor=int(data[0:16],2)
	endDoor=int(data[16:32],2)
	comp=int(data[32:48],2)
	checksum=int(data[48:64],2)
	seq = int(data[64:65],2)
	lastData=data
	data=int(data[65:97],2)

	sum = functions.checksum(originDoor,endDoor,comp)

	i+=1
	os.system('clear')
	print("\n------------------------------------------")
	print("\tEnvio do",i,"º pacote")
	print("------------------------------------------")

	if (seq==0):
		print("\nPacote ["+str(lastData)+"] duplicado! Descartando e re-solicitando...")
		duplicatedDatas.append(lastData)
	if (sum!=checksum):
		print("\nPacote ["+str(data)+"] com erro de bits! Descartando e re-solicitando...")
		corruptedDatas.append(data)
	while (seq==0 or sum!=checksum):
		try :
			#Enviando mensagem ao cliente
			server.sendto(msg.encode("ascii"), addr)
		except socket.error as msg:
			print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
			sys.exit()
		
		# Recebendo datas do cliente (datas, endereço)
		d = server.recvfrom(pack_size)
		data = d[0]
		addr = d[1]
		if not data: 
			break

		#Extraindo datas do pacote
		originDoor=int(data[0:16],2)
		endDoor=int(data[16:32],2)
		comp=int(data[32:48],2)
		checksum=int(data[48:64],2)
		seq = int(data[64:65],2)
		lastData=data
		data=int(data[65:97],2)

		sum = functions.checksum(originDoor,endDoor,comp)

	if (seq==1 and sum==checksum):
		recivedData.append(data)
		recivedDataOrder.append(str(data) + "\n")
		recivedDataOrder.sort()
		print("\nPacote ["+str(data)+"] recebido corretamente!")
		print("\nPacotes recebidos até o momento:")
		print(recivedData)
		print("\nPacotes duplicados:")
		print(duplicatedDatas)
		print("\nPacotes corrompidos:")
		print(corruptedDatas)

		msg = functions.creat_pack_server(server.getsockname()[1],port,server_size,1,1)
		try :
			#Enviando mensagem ao cliente informando pacote duplicado/corrompido
			server.sendto(msg.encode("ascii"), addr)
		except socket.error as msg:
			print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
			sys.exit()

server.close()
