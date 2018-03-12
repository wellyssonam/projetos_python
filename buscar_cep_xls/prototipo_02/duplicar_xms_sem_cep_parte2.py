# PYTHON 2
# -*- coding: utf-8 -*-
import xlwt
import ast
import os

file = os.path.dirname(os.path.abspath(__file__))
# leitura de arquivo
myfile = open(file + "/cliente_01_com_cep.txt", "r")
lista = ast.literal_eval(myfile.read())
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet(u"res")
map(lambda x: map(lambda y: worksheet.write(x, y, str(lista[x][y]).decode("utf-8")), range(len(lista[x]))), range(len(lista)))
workbook.save(u"cliente_01_com_cep.xls")