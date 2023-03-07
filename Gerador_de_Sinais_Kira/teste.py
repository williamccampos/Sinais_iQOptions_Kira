# coding=utf-8
import telebot
from iqoptionapi.stable_api import IQ_Option
import threading
import re
from datetime import datetime, date
from telebot import types
import websocket
import requests
import sys

session_dict = {}

######################### CONEXÃO COM IQ OPTION ################################################################

def is_valid_email(email):
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None


######################### CONEXÃO COM TELEBOT POR TOKEN ########################################################
bot = telebot.TeleBot('6139012508:AAF4uP6NN1SnYCxolj3hPltEL5ngaLpVNoM')

@bot.message_handler(commands=['start'])
def start_handler(session):
    keyboard = types.InlineKeyboardMarkup()
    login_button = types.InlineKeyboardButton(text='Entrar IQOptions', callback_data='entrar')

    keyboard.row(login_button)
    bot.send_message(session.chat.id, 'Olá seja bem vindo, Ao bot **** Para continuar faça o login em sua conta', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'entrar')
def handle_login_callback(call):
   login_handler(call.message)

def handle_login(session):
    bot.send_message(session.chat.id, "Digite seu e-mail do IQ Option:")
    bot.register_next_step_handler( session, lambda message: get_password(session, message.text))


def get_password(session, email_input):
    global email
    if not is_valid_email(email_input):
        bot.send_message(
            session.chat.id, "E-mail inválido. Digite um e-mail válido.")
        return handle_login(session)
    email = email_input
   
    bot.send_message(session.chat.id, "Digite sua senha do IQ Option:")
    bot.register_next_step_handler(
        session, lambda message: iq_login(session, message.text))


def iq_login(session, password_input):
    global email, password, API
    password = password_input
    print(email)
    API = IQ_Option(email, password)
    API.connect()
    if not API.connect():
        bot.send_message(
            session.chat.id, "Falha ao conectar ao IQ Option. Verifique seu e-mail e senha.")
        return
    if not API.check_connect():
        bot.send_message(
            session.chat.id, "Senha incorreta. Verifique seu e-mail e senha.")
        API = None
        return


    
    # Create a new session for the user
    session_dict[session.chat.id] = []

    saldo = API.get_balance()
    # Verifica se o usuário já tem uma sessão e cria uma nova sessão se necessário
    if session.chat.id not in session_dict:
        session_dict[session.chat.id] = []
        saldo = session_dict[session.chat.id]
    print(API.get_balance());
    bot.send_message(session.chat.id, f"Seu saldo atual é de {saldo}")

@bot.message_handler(commands=['login'])
def login_handler(session):
    if session.chat.id in session_dict:
        bot.send_message(
            session.chat.id, "Você já está conectado ao IQ Option. Use o comando /logout para sair da sua sessão atual.")
        print(API.get_balance())
        return
    # Inicia uma nova thread para lidar com o login
    threading.Thread(target=handle_login, args=(session,)).start()

bot.polling()
