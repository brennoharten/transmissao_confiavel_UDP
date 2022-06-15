import socket, os, sys, functions, random

door = 5000
HOST = '127.0.0.1'
pack_size = 150
comp = 97

#filename = "./arquivo-enviar/foguete.txt"

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockDoor = 0
client.bind(('',sockDoor))
originDoor = client.getsockname()[1]
client.connect((HOST,door))
file = open(sys.argv[1],'r')
filename = sys.argv[1]

#envio do cabecalho para criacao do arquivo
filesize = os.path.getsize(filename)
client.send(filename.encode())
client.send(f"{filesize}".encode())

vector = file.read().splitlines()

while len(vector)>1:

    option = functions.menu(vector)
    #Estado 0

    dado = int(vector.pop(0))
    if (option ==2):
        sum=0
    else:
        sum = functions.checksum(originDoor,door,comp)
    if (option==3):
        seq=1
    else:
        seq=0

    if option==4:
        sys.exit()
        
    msg = functions.creat_pack_client(originDoor,door,comp,sum,seq,dado)
    try :
        client.sendto(msg.encode("ascii"), (HOST, door))
    except socket.error as msg:
        print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
        sys.exit()

    
    #Estado 1
    d = client.recvfrom(pack_size)
    data = d[0]
    addr = d[1]

    if not data: 
        break

    originDoorServer=int(data[0:16],2)
    endDoorServer=int(data[16:32],2)
    sizeServer=int(data[32:48],2)
    ackServer=int(data[48:49],2)
    seqServer=int(data[49:50],2)
    sumServer=int(data[50:66],2)


    checkSUM=functions.checksum(originDoorServer,endDoorServer,sizeServer)

    while (sumServer!=checkSUM or (ackServer==1 and seqServer==1)):

        sum = functions.checksum(originDoor,door,comp)
        seq = 0
        msg = functions.creat_pack_client(originDoor,door,comp,sum,seq,dado)
        client.sendto(msg.encode("ascii"),(HOST,door))		

        # Recebendo mensagem do servidor
        d = client.recvfrom(pack_size)
        data = d[0]
        addr = d[1]

        originDoorServer=int(data[0:16],2)
        endDoorServer=int(data[16:32],2)
        sizeServer=int(data[32:48],2)
        ackServer=int(data[48:49],2)
        seqServer=int(data[49:50],2)
        sumServer=int(data[50:66],2)

        checkSUM=functions.checksum(originDoorServer,endDoorServer,sizeServer)

        if not data: 
            break

    #Estado 2

    option = functions.menu(vector)
    while (option==4):
        toshuffle = vector[0:len(vector)-1]
        random.shuffle(toshuffle)
        toshuffle.append('-1')
        vector=toshuffle
        option = functions.menu(vector)

    dado = int(vector.pop(0))
    if dado==-1:
        break

    #Forçar o erro de bits mudando a sum de verificação
    if (option==2):
        sum=0
    else:
        sum = functions.checksum(originDoor,door,comp)

    #Forçando pacotes duplicados
    if (option==3):
        seq=0
    else:
        seq=1

    #Encerrando client
    if option==4:
        sys.exit()


    msg = functions.creat_pack_client(originDoor,door,comp,sum,seq,dado)

    try :
        #Enviando datagrama ao servidor
        client.sendto(msg.encode("ascii"), (HOST, door))
    except socket.error as msg:
        print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
        sys.exit()

    #Estado 3
    # Recebendo mensagem do servidor
    d = client.recvfrom(pack_size)
    data = d[0]
    addr = d[1]

    if not data: 
        break

    originDoorServer=int(data[0:16],2)
    endDoorServer=int(data[16:32],2)
    sizeServer=int(data[32:48],2)
    ackServer=int(data[48:49],2)
    seqServer=int(data[49:50],2)
    sumServer=int(data[50:66],2)

    checkSUM=functions.checksum(originDoorServer,endDoorServer,sizeServer)

    while (sumServer!=checkSUM or (ackServer==1 and seqServer==0)):

        sum = functions.checksum(originDoor,door,comp)
        seq = 1
        msg = functions.creat_pack_client(originDoor,door,comp,sum,seq,dado)
        client.sendto(msg.encode("ascii"),(HOST,door))		

        # Recebendo mensagem do servidor
        d = client.recvfrom(pack_size)
        data = d[0]
        addr = d[1]

        originDoorServer=int(data[0:16],2)
        endDoorServer=int(data[16:32],2)
        sizeServer=int(data[32:48],2)
        ackServer=int(data[48:49],2)
        seqServer=int(data[49:50],2)
        sumServer=int(data[50:66],2)

        checkSUM=functions.checksum(originDoorServer,endDoorServer,sizeServer)

        if not data: 
            break

client.close()