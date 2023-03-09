# coding=utf-8
import telebot
from iqoptionapi.stable_api import IQ_Option
#import threading
import re
from datetime import datetime, date
from telebot import types
import websocket
import requests
import sys

######################### CONEXÃO COM TELEBOT POR TOKEN ########################################################
bot = telebot.TeleBot('6139012508:AAF4uP6NN1SnYCxolj3hPltEL5ngaLpVNoM')

# criando um dicionário para armazenar as informações da sessão
session_dict = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    login_button = types.InlineKeyboardButton(
        text='Entrar IQOptions', callback_data='entrar')

    keyboard.row(login_button)
    bot.send_message(message.chat.id, 'Olá seja bem vindo, Ao bot **** Para continuar faça o login em sua conta', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'entrar')
def handle_login_callback(call):
    login_handler(call.message)

    @bot.message_handler(commands=['login'])
    def login_handler(message):
        chat_id = message.chat.id
        print(f"Chat ID: {chat_id}")
        bot.send_message(message.chat.id, "Digite seu e-mail do IQ Option:")
        session_dict[message.chat.id] = {}
        session_dict[message.chat.id]['usuario'] = 'email'
    pass

@bot.message_handler(func=lambda message: session_dict.get(message.chat.id, {}).get('usuario') == 'email')
def receber_password(message):
    bot.send_message(message.chat.id, "Digita sua senha da IQ Options:")
    session_dict[message.chat.id]['usuario'] = 'password'

    @bot.message_handler(func=lambda message: session_dict.get(message.chat.id, {}).get('usuario') == 'password')
    def iq_login(message):
        API = IQ_Option('','')
        API.connect()
        API.change_balance('PRACTICE') # PRACTICE / REAL
        if API.check_connect():
	        print(' Conectado com sucesso!')
        else:
	        print(' Erro ao conectar')
	        input('\n\n Aperte enter para sair')
        return

        saldo = API.get_balance()
        bot.send_message(message.chat.id, f"Seu saldo atual é de {saldo}")



def login_handler(message):
    if message.chat.id in session_dict:
        bot.send_message(message.chat.id, "Você já está conectado ao IQ Option. Use o comando /logout para sair da sua sessão atual.")
        print(API.get_balance())
    return
    # Inicia uma nova thread para lidar com o login
    #threading.Thread(target=handle_login, args=(message)).start()

bot.polling(timeout=30)
