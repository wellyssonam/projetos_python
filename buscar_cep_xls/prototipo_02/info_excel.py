# PYTHON 3
# -*- coding: utf-8 -*-
from xlrd import xlrd
import os
from unicodedata import normalize

uf, cidade, logradouro, bairro = False, False, False, False
file = os.path.dirname(os.path.abspath(__file__)) + '/clientes_01_original.xls'
xls = xlrd.open_workbook(file, 'rb')
# pega a primeira linha do arquivo
plan, dic, cont = xls.sheet_by_index(0), {}, 0
sem_cep, vazio = 0, 0
dic_res_finded = {}

for x in range(12573):
	if x != 0:
		print ("\n")
		print (cont + 2)
		#x = plan.cell_value(x, 0)
		linha = plan.row_values(x)
		# INFORMAÇÕES DA PLANILHA NA ORDEM DE 0 A 15
		# NOMES	CELULAR1	ENDERECO	NUMERO	COMPLEMENTO	BAIRRO	CIDADE	UF	CODIGO MUNICIPIO	PAIS	DTACADASTRO
		# PESSOA	CELULAR2	PONTOREFERENCIA	CEP

		uf, cidade, logradouro, bairro, complemento, cep = linha[7], linha[6], linha[2], linha[5].lower(), linha[4], linha[15]

		# faz uma requisição usando o "opener"
		"""
		print ("\n" + uf)
		print (cidade)
		print (logradouro)
		"""
		print (logradouro)
		logradouro = logradouro.lower()
		if (logradouro == "" and cep == "") or (bairro == "desconhecido" and cep == ""):
			logradouro = "vazio"
			vazio += 1
		elif cep == "":
			sem_cep += 1

		if cep != "":
			dic_res_finded[cont + 2] = cep
		elif cep == "":
			logradouro_original = logradouro

			if logradouro[0:3] == "ua ":
				logradouro = "rua " + logradouro[3:]

			if logradouro[0:3] == "av ":
				logradouro = "avenida " + logradouro[3:]

			if logradouro[0:4] == "av. ":
				logradouro = "avenida " + logradouro[4:]

			if logradouro[0:3] == "ru ":
				logradouro = "rua " + logradouro[3:]
			
			if logradouro.__contains__(" - "):
				logradouro = logradouro[0:logradouro.find(" - ")]

			if logradouro.__contains__(" -"):
				logradouro = logradouro[0:logradouro.find(" -")]

			if logradouro.__contains__("aven "):
				logradouro = logradouro.replace("aven ", "avenida ")

			if logradouro.__contains__("conj "):
				logradouro = logradouro.replace("conj ", "conjunto ")

			if logradouro.__contains__(" loteam"):
				logradouro = logradouro[0:logradouro.find(" loteam")]

			if logradouro.__contains__(" loteamento"):
				logradouro = logradouro[0:logradouro.find(" loteamento")]

			if logradouro.__contains__(" cond "):
				logradouro = logradouro[0:logradouro.find(" cond ")]

			if logradouro.__contains__(" cond."):
				logradouro = logradouro[0:logradouro.find(" cond.")]

			if logradouro.__contains__(" condom."):
				logradouro = logradouro[0:logradouro.find(" condom.")]

			if logradouro.__contains__(" condominio"):
				logradouro = logradouro[0:logradouro.find(" condominio")]

			if logradouro.__contains__(" quadra"):
				logradouro = logradouro[0:logradouro.find(" quadra")]

			if logradouro.__contains__(" q-"):
				logradouro = logradouro[0:logradouro.find(" q-")]

			if logradouro.__contains__(" casa"):
				logradouro = logradouro[0:logradouro.find(" casa")]

			if logradouro.__contains__(" c-"):
				logradouro = logradouro[0:logradouro.find(" c-")]

			if logradouro.__contains__(" bloco "):
				logradouro = logradouro[0:logradouro.find(" bloco ")]

			if logradouro.__contains__(" bl - "):
				logradouro = logradouro[0:logradouro.find(" bl- ")]

			if logradouro.__contains__(" ap - "):
				logradouro = logradouro[0:logradouro.find(" ap - ")]

			if logradouro.__contains__(" - apto "):
				logradouro = logradouro[0:logradouro.find(" - apto ")]

			if logradouro.__contains__(" apto "):
				logradouro = logradouro[0:logradouro.find(" apto ")]

			if logradouro.__contains__("des."):
				logradouro = logradouro.replace("des.", "desembargador")

			if logradouro.__contains__("dr."):
				logradouro = logradouro.replace("dr.", "doutor")

			if logradouro.__contains__(" dr "):
				logradouro = logradouro.replace(" dr ", " doutor ")

			if logradouro.__contains__(" cel "):
				logradouro = logradouro.replace(" cel ", " coronel ")

			if logradouro.__contains__(" dep "):
				logradouro = logradouro.replace(" dep ", " deputado ")

			if logradouro.__contains__(" gov "):
				logradouro = logradouro.replace(" gov ", " governador ")

			if logradouro.__contains__(" pres "):
				logradouro = logradouro.replace(" pres ", " presidente ")

			if logradouro.__contains__(" prof "):
				logradouro = logradouro.replace(" prof ", " professor ")

			if logradouro.__contains__(" com "):
				logradouro = logradouro.replace(" com ", " ")

			if logradouro.__contains__(": "):
				logradouro = logradouro.replace(": ", " ")

			if logradouro.__contains__(". "):
				logradouro = logradouro.replace(". ", " ")

			if logradouro.__contains__("  "):
				logradouro = logradouro.replace("  ", " ")

			#bairro = normalize("NFKD", bairro).encode("ASCII", "ignore").decode("ASCII")
			#logradouro = normalize("NFKD", logradouro).encode("ASCII", "ignore").decode("ASCII")
			print (logradouro)

			#{"rua": {"bairro": [linha]}}
			if not dic.keys().__contains__(logradouro):
				dic[logradouro] = {bairro: [cont + 2]}
			elif not dic[logradouro].__contains__(bairro):
				dic[logradouro][bairro] = [cont + 2]
			else:
				dic[logradouro][bairro].append(cont + 2)

		cont += 1

print ("\ntotal: " + str(cont))

texto_corrigir = ""
"""
for key in dic.keys():
	print (key + "\n" + str(dic[key]) + "\n")
	#texto_corrigir += (key + " " + str(erro[key]) + "\n")
"""

print ("\n========================= RESULTADOS ================================\n")
print ("total de chaves: " + str(len(dic.keys())))
print ("total de endereços: " + str(12572))
print ("total de logradouro vazio: " + str(vazio))
print ("total ainda desconhecido: " + str(sem_cep))
print ("total encontrado: " + str(12572 - sem_cep - vazio))
print ("\n")

# Escrever no arquivo texto as correções que deverão ser feitas
myfile = open("info.txt", "w")
myfile.write(str(dic))
myfile.close()

myfile = open("resultado_encontrado.txt", "w")
myfile.write(str(dic_res_finded))
myfile.close()

erro = ""
myfile = open("erro.txt", "w")

for log in sorted(dic.keys()):
	erro += log + " => "
	for bairro in sorted(dic[log].keys()):
		erro += "[" + bairro + "], "
	erro += "\n"

myfile.write(erro)
myfile.close()
