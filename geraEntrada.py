# -*- coding: utf-8 -*-
import random

arquivo = open('entrada', 'w')
npacotes = input("Informe o número de pacotes a serem gerados: ")
numero = random.randint(1, 1000)

for i in range(0,int(npacotes)):
	arquivo.write(str(numero+i)+"\n")
arquivo.write("-1\n")

arquivo.close()



