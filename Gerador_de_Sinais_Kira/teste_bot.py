import telebot
from iqoptionapi.stable_api import IQ_Option
from telebot import types

API_TOKEN = '6139012508:AAF4uP6NN1SnYCxolj3hPltEL5ngaLpVNoM'

bot = telebot.TeleBot(API_TOKEN)

users = {}
assets = ['EURUSD', 'AUDCAD', 'GBPUSD']

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bem-vindo ao bot! Para começar, digite /login.")
    print('Bot iniciado!')

@bot.message_handler(commands=['login'])
def login_handler(message):
    cid = message.chat.id
    if cid in users and users[cid]['logged_in']:
        bot.reply_to(message, "Você já está logado.")
        return

    bot.reply_to(message, "Por favor, digite seu email:")
    bot.register_next_step_handler(message, email_handler)

def email_handler(message):
    cid = message.chat.id
    email = message.text
    users[cid] = {'email': email}
    bot.reply_to(message, "Agora, digite sua senha:")
    bot.register_next_step_handler(message, password_handler)

def password_handler(message):
    cid = message.chat.id
    password = message.text

    # Verifica se a chave 'email' existe no dicionário do usuário
    if 'email' not in users[cid]:
        bot.reply_to(message, "Por favor, digite seu email primeiro.")
        return

    # Cria a chave 'password' no dicionário do usuário
    users[cid].setdefault('password', password)

    # Cria a chave 'api' no dicionário do usuário
    users[cid].setdefault('api', IQ_Option(users[cid]['email'], users[cid]['password']))
    
    # Cria a chave 'logged_in' no dicionário do usuário
    users[cid].setdefault('logged_in', users[cid]['api'].connect())

    if not users[cid]['logged_in']:
        bot.reply_to(message, "Login inválido.")
        return

    balance = users[cid]['api'].get_balance()
    bot.reply_to(message, f"Seu saldo é de {balance} dólares.")

@bot.message_handler(commands=['change_account'])
def change_account_handler(message):
    cid = message.chat.id
    if cid not in users:
        bot.reply_to(message, "Você não está logado.")
        return

    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('Conta Real'))
    markup.row(types.KeyboardButton('Conta Demo'))
    bot.reply_to(message, "Selecione a conta que deseja utilizar:", reply_markup=markup)
    bot.register_next_step_handler(message, account_handler)

def account_handler(message):
    cid = message.chat.id
    account = message.text
    if account == 'Conta Real':
        users[cid]['api'] = IQ_Option(users[cid]['email'], users[cid]['password'])
    elif account == 'Conta Demo':
        users[cid]['api'] = IQ_Option(users[cid]['email'], users[cid]['password'])
    else:
        bot.reply_to(message, "Opção inválida.")
    return

    users[cid]['logged_in'] = users[cid]['api'].connect()
    if not users[cid]['logged_in']:
        bot.reply_to(message, "Login inválido.")
    return
    balance = users[cid]['api'].get_balance()
    bot.reply_to(message, f"Seu saldo é de {balance} dólares.")

@bot.message_handler(commands=['buy'])
def buy(message):
    cid = message.chat.id
    if cid not in users or not users[cid]['logged_in']:
        bot.reply_to(message, "Você precisa estar logado para comprar.")
        return

    # Pergunta qual ativo deseja comprar
    markup = types.ReplyKeyboardMarkup()
    for asset in assets:
        markup.row(types.KeyboardButton(asset))
    bot.reply_to(message, "Escolha o ativo que deseja comprar:", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: buy_asset_handler(msg, cid))

def buy_asset_handler(message, cid):
    asset = message.text
    if asset not in assets:
        bot.reply_to(message, "Ativo inválido.")
        return

    bot.reply_to(message, f"Você escolheu o ativo {asset}. Qual valor você quer comprar?")
    bot.register_next_step_handler(message, lambda msg: buy_amount_handler(msg, cid, asset))

def buy_amount_handler(message, cid, asset):
    try:
        amount = float(message.text)
    except ValueError:
        bot.reply_to(message, "Valor inválido.")
        return

    # Realiza a compra
    response, order_id = users[cid]['api'].buy(amount, asset, "digital", "open")

    if response:
        bot.reply_to(message, f"Compra realizada com sucesso! Ordem ID: {order_id}")
    else:
        bot.reply_to(message, "Erro ao realizar a compra.")

@bot.message_handler(commands=['balance'])
def balance_handler(message):
    cid = message.chat.id
    if cid not in users or not users[cid]['logged_in']:
        bot.reply_to(message, "Você precisa estar logado para visualizar o saldo.")
    return
    balance = users[cid]['api'].get_balance()
    bot.reply_to(message, f"Seu saldo é de {balance} dólares.")

bot.polling()
