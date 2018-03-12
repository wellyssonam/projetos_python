# PYTHON 2
# -*- coding: utf-8 -*-
import xlwt
import ast
import os

file = os.path.dirname(os.path.abspath(__file__))
# leitura de arquivo
myfile = open(file + "/resultado.txt", "r")
dic = ast.literal_eval(myfile.read())

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet(u"res")

for key in dic.keys():
	worksheet.write(key-1, 0, dic[key])

workbook.save("clientes_01_aux.xls")