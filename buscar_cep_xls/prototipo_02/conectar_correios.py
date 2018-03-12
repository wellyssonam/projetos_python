# PYTHON 2
# -*- coding: utf-8 -*-
#from xlrd import xlrd
import os
import ast
from unicodedata import normalize
from urllib2 import urlopen, Request
from urllib import urlencode
import time

dic_res = {}
file = os.path.dirname(os.path.abspath(__file__))
# leitura de arquivo
myfile = open(file + "/info.txt", "r")
myfileres = open(file + "/resultado_encontrado.txt", "r")

dic = ast.literal_eval(myfile.read())
dic_res = ast.literal_eval(myfileres.read())

nao_existe = []
cont, encontrou = 0, 0
headers = {'Authorization': 'Token token=a57099e5d744ffa8b095913f49006436'}
# Pesquisa de CEP por estado, cidade e logradouro
print len(dic.keys())
for logradouro in dic.keys()[0:]:
	if cont < 0:
		print cont
		cont += 1
	else:
		print cont
		if logradouro not in ["desconhecido", "null", "vazio"]:
			for bairro in dic[logradouro].keys():
				#print logradouro
				#print bairro
				#print dic[logradouro][bairro]
				params = {'estado': 'PI', 'cidade': 'Teresina', 'logradouro': logradouro, 'bairro': bairro}
				print (dic[logradouro][bairro])
				url = "http://www.cepaberto.com/api/v2/ceps.json?%s" % (urlencode(params))
				print params
				json = urlopen(Request(url, None, headers=headers)).read()
				if json.__contains__("null"):
					json = json.replace("null", "False")
				print json
				json = ast.literal_eval(json)
				if len(json.keys()) > 0:
					print json["bairro"]
					for i in dic[logradouro][bairro]:
						dic_res[i] = json["cep"]
						encontrou += 1
					print "\n"
				time.sleep(5)

		else:
			for bairro in dic[logradouro].keys():
				for i in dic[logradouro][bairro]:
					dic_res[i] = "VAZIO"
					encontrou += 1
					print "VAZIO"
		cont += 1

print "\ntotal encontrado incluindo vazio: " + str(len(dic_res.keys()))
print "\nencontrou: " + str(encontrou)

myfile = open("resultado.txt", "w")
myfile.write(str(dic_res))
myfile.close()