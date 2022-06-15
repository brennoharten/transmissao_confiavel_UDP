import os

def menu(vetor):
	os.system('clear')
	print("\n----------------------------------------------")
	print("pacotes para enviar: ")
	print(vetor[0:len(vetor)-1])
	print("\nOpções:")
	print("\n1 - Enviar pacote")
	print("2 - Corromper pacote")
	print("3 - Duplicar pacote")
	print("4 - Sair\n")
	option = 0
	while (option<1 or option>5):
		option = int(input("Opção escolhida: "))
	return option

def complement(n,size):
	comp = n ^ ((1 << size) - 1)
	return '0b{0:0{1}b}'.format(comp, size)

def checksum(originDoor,endDoor,size):
	firstsum = bin(originDoor + endDoor)[2:].zfill(16)
	if (len(firstsum)>16):
		firstsum = firstsum[1:17]
		firstsum = bin(int(firstsum,2) + 1)[2:].zfill(16)
	secondsum = bin(int(firstsum,2)+size)[2:].zfill(16)
	if (len(secondsum)>16):
		secondsum = secondsum[1:17]
		secondsum = bin(int(secondsum,2) + 1)[2:].zfill(16)
	checksum = complement(int(secondsum,2),16)[2:]
	return int(checksum,2)

def creat_pack_client(originDoor,endDoor,size,sum,seq,dado):
	pack = bin(originDoor)[2:].zfill(16)+bin(endDoor)[2:].zfill(16)+bin(size)[2:].zfill(16)+bin(sum)[2:].zfill(16)+bin(seq)[2:].zfill(1)+bin(dado)[2:].zfill(32)
	return pack

def creat_pack_server(originDoor,endDoor,size,ack,seq):
	sum = checksum(originDoor,endDoor,size)
	pack = bin(originDoor)[2:].zfill(16)+bin(endDoor)[2:].zfill(16)+bin(size)[2:].zfill(16)+bin(ack)[2:].zfill(1)+bin(seq)[2:].zfill(1)+bin(sum)[2:].zfill(16)
	return pack