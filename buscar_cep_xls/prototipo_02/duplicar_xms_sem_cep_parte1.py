# PYTHON 3
# -*- coding: utf-8 -*-
from xlrd import xlrd
import os

file_origem = os.path.dirname(os.path.abspath(__file__)) + '/clientes_01_original.xls'
xls = xlrd.open_workbook(file_origem, 'rb')
# pega a primeira linha do arquivo
plan = xls.sheet_by_index(0)
lista = []

for x in range(12573):
	if x != 0:
		linha = plan.row_values(x)
		if linha[15] is not "":
			lista.append(linha)

print ("\n========================= RESULTADOS ================================\n")
print ("total de ceps: " + str(len(lista)))
print ("\n")

myfile = open("cliente_01_com_cep.txt", "w")
myfile.write(str(lista))
myfile.close()
