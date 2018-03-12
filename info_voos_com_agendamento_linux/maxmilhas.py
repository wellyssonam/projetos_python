# -*- encoding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from datetime import date, datetime
import smtplib
import os

"""
Keys = fornece atalhos do teclado como RETURN, F1, ALT, etc
"""

class Maxmilhas():
    """
    - Este programa será executado no arquivo de rotinas do linux localizado em /etc/crontab, basta adicionar
    a linha logo abaixo ...
    0 8-23  * * *   root       DISPLAY=:0 python /caminho_ate_arquivo/maxmilhas.py
    este programa será executado a partir das 8:00 às 23:00 em intervalos de 1 hora.

    - O programa ao iniciar só será executado por completo caso ainda não tenha sido executada no dia, isso é
    verificado pois ao ser executado pela primeira vez cria-se um arquivo que ficará oculta e o conteúdo deste
    será a data de execução, se a data for diferente o programa será executado por completo e a data será
    atualizada.

    - Este programa utiliza a biblioteca do selenium para poder acessar o site escolhido no caso maxmilhas,
    insiro o link que aparece após a escolha da origem, destino, data e clicar no botão buscar, essa tomada
    de decisão foi escolhida pois após clicar no botão buscar já iremos utilizar o link onde nele estarão contidas
    todas as informações da busca do vôo.

    - Utiliza-se também a biblioteca smtplib para enviar essas informações para e-mail específico, o usuário terá apenas
    que mudar as varíáveis com as informações do e-mail na função send_message.
    """

    def __init__(self):
        if not self.already_executed():
            # abre a página do navegador em bakground, não irá atrapalhar o usuário caso esteja fazendo outra atividade
            display = Display(visible=0, size=(1024, 768))
            display.start()

            info = self.open_maxmilhas()

            display.stop() # encerra o display que esconde o navegador

            self.send_message(info)

    def already_executed(self):
        file_name = ".maxmilhas_date_info.txt"
        path = os.path.dirname(os.path.abspath(__file__)) + "/"

        if file_name not in os.listdir(path):
            file = open(path + file_name, "w")
            file.write(str(date.today()))
            file.close()
            return False
        else:
            info = open(path + file_name, "r").read()
            if datetime.strptime(info + " 00:00:00", "%Y-%m-%d %H:%M:%S").date() == date.today():
                return True

            file = open(path + file_name, "w")
            file.write(str(date.today()))
            file.close()
            return False
            # file = open(path + file_name, "w")


    def open_maxmilhas(self):
        driver = webdriver.Chrome()
        driver.get("https://www.maxmilhas.com.br/busca-passagens-aereas/OW/THE/FLN/2018-05-19/1/0/0/EC")

        time.sleep(10) # Pause to allow you to inspect the browser.
        quant_flights = 5
        txt = "Origem: Teresina - Destino: Florianopolis - Data Ida: 2018-05-19\n\n"
        txt += "Companhia\tOrigem\tPartida\tDestino\tChegada\tValor\n"
        companies = driver.find_elements_by_css_selector(".flight-item .container-fluid .row .flight-item-information .row .v-center-columns span.airline-name")
        time_start_end = driver.find_elements_by_css_selector(".flight-item .container-fluid .row .flight-item-information .row .v-center-columns span.flight-time")
        origin_destiny = driver.find_elements_by_css_selector(".flight-item .container-fluid .row .flight-item-information .row .v-center-columns span.flight-destination")
        values = driver.find_elements_by_css_selector(".savings-tag-wrapper button span")

        for index in range(quant_flights):
            txt += companies[index].get_attribute('innerHTML') + "\t\t"
            txt += origin_destiny[index if index == 0 else index*2].get_attribute('innerHTML') + "\t"
            txt += time_start_end[index if index == 0 else index*2].get_attribute('innerHTML') + "\t"
            txt += origin_destiny[index + 1 if index == 0 else index*2+1].get_attribute('innerHTML') + "\t"
            txt += time_start_end[index + 1 if index == 0 else index*2+1].get_attribute('innerHTML') + "\t"
            value = values[index].get_attribute('innerHTML')
            while(True):
                ini = value.find("<")
                fim = value.find(">")
                if ini == -1: break
                value = value.replace(value[ini:fim+1], "")
            txt += value + "\n"

        # print txt

        # "close" para quando utiliza-se uma tab, "quit" para mais de uma tab ser fechada ao mesmo tempo
        # time.sleep(5) # Pause to allow you to inspect the browser.
        driver.close()
        return txt

    def send_message(self, text):
        sender = "example@example.com"
        receivers = ["example@example.com"]
        subject = "MAXMILHAS - TERESINA TO FLORIANÓPOLIS"
        message = "MAXMILHAS - TERESINA TO FLORIANÓPOLIS - INFOMATIONS\n\n"
        message += text.encode("utf-8")
        # print message

        try:
            smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(user=sender, password="here your password")
            smtpObj.sendmail(sender, receivers, message)
            smtpObj.quit()
            print "Email enviado com sucesso"

        except:
            print "Não foi possível enviar a mensagem !!!"
            raise

        return

# Dando ìnicio as execuções das funções
Maxmilhas()