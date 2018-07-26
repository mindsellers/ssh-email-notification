#!/usr/bin/python
# -*- coding: utf-8 -*-

from configparser import SafeConfigParser
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import os
import sys


def getconfig(conf='send.conf'): #читаем конфиг
    configfile=os.path.abspath(os.path.dirname(__file__))+'/'+conf #из файла, 
    #переданного функции, в том же каталоге, что и скрипт
    parser = SafeConfigParser()
    try:
        parser.read(configfile)
        params=dict()
	serverconf=dict(parser.items('server')) #получаем секцию server
	messageconf=dict(parser.items('message')) #получаем секцию message
	return serverconf,messageconf
    except Exception as s:
        print 'Cannot read config file!'
	print s
    
def sendmail(serverconf,messageconf,message): #функция отправки почты
    msg = MIMEText(message, 'plain', 'utf-8') #формируем письмо для корректной отправки
    msg['Subject'] = Header(messageconf['subj'], 'utf-8')
    msg['From'] = serverconf['login']
    msg['To'] = str(messageconf['dest'])
    
    server = smtplib.SMTP(serverconf['server'],int(serverconf['port'])) #создаем экземпляр класса
    server.login(serverconf['login'],serverconf['pass'])                #логинимся
    server.sendmail(serverconf['login'],list(messageconf['dest'].split(',')), msg.as_string()) 
    #отправляем почту и отключаемся
    server.quit()



if __name__=='__main__':
    serverconf,messageconf=getconfig()
    date,login,user=sys.argv[1:]
    ip=login.split(' ')[0] 
    srvip=login.split(' ')[2] 
    if '10.10.10.' in ip: # не будем слать письмо, если логин был из админской сети
	pass

    else:
	message='!!!ВНИМАНИЕ!!!\n' + \
	date+'\nОсуществлен логин с адреса '+ip \
        +'\nПод учеткой '+user + \
	'\nНа сервер '+srvip
	sendmail(serverconf,messageconf,message)
