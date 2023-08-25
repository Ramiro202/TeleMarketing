
import pyfiglet
from os import system
from time import sleep
from random import randint
from dotenv import dotenv_values
from telethon.tl.types import Channel
from telethon.sync import TelegramClient
from telethon.tl.types import ChannelParticipantsRecent

env = dotenv_values(".env")
api_id = env["API_ID"]
api_hash = env["API_HASH"]
phone_number = env["PHONE"]

system("clear || cls")

try:
	# Criar uma instância do cliente
	client = TelegramClient("session_name", api_id, api_hash)
	# Iniciar o cliente
	client.connect()
	
except ConnectionError:
	print("=="*20)
	print("\033[1;31mERRO | Falha na conexão a internet\033[m")
	exit()

if not client.is_user_authorized():
    # Se não tiver conectado vai receber
    # O código de confirmação pelo telegram
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Digite o codigo enviado: '))

def banner():
	user = client.get_me()
	print("\033[1;34mby: https://t.me/ramirosegunda\033[m")
	print("??"*25)
	text = pyfiglet.figlet_format("Disparo \nTelegram", width=50, justify="center")
	print("\033[1;34m", text, "\033[m")
	print("=="*25)
	print(f"\033[1;32m{'O grupo que selecionares o programa irá se'.center(50)}")
	print(f"{'incarregar de pegar tudos os membros do mesmo'.center(50)}")
	print(f"{'e mandar a tua mensagem para ele!'.center(50)}\033[m")
	print("--"*25)
	print(f"\033[1;34mUsuário: {user.first_name} {f'({user.username})'.rjust(32)}")
	print("~~"*25)

def testo():
    arquivo = open(env["MESSAGE"], 'rt')
    text = arquivo.read()
    return text

def GetDialogs():
	lista = []
	dados = {}
    # Obter uma lista de diálogos (conversas)
	dialogs = client.get_dialogs()

	# Filtrar e exibir apenas os grupos
	for dialog in dialogs:
		if isinstance(dialog.entity, Channel):
			group = dialog.entity
			dados = {"name_group": group.title, "chat_id": group.id}
			lista.append(dados)
	return lista

def varrer_group(chat_id):
	grupos = []
	conjunto = {}
	# Obter a lista de participantes do grupo
	participants = client.get_participants(chat_id, filter=ChannelParticipantsRecent)

	# Exibir os IDs dos participantes
	for participant in participants:
		conjunto = {"nome": participant.first_name, "id": participant.id}
		grupos.append(conjunto)

	return grupos

def send_mensagem(user_id, msg):
	try:
		client.send_message(user_id, msg)
		return True
	except:
		return False


while True:
	system("clear || cls")
	banner()
	grupos = GetDialogs()

	for number, grupo in enumerate(grupos):
		print(f'{number} - {grupo["name_group"]}')
	print("=="*25)

	numero = input("Selecione o grupo => ")
	print("=="*25)

	if numero == "*":
		for c in range(0, len(grupos)):
			try:
				pessoas = varrer_group(grupos[c]["chat_id"])
			except:
				print("\033[1;31mNúmero invalido!\033[m")
				break

			msg = testo()
			print(f"A mensagem sera enviada para {len(pessoas)}")
			print("__"*25)

			for pessoa in pessoas:
				mensagem = send_mensagem(pessoa["id"], msg)
				if mensagem:
					print(f"\033[1;32mMensagem enviada para {pessoa['nome']}\033[m")
					sleep(randint(3, 10))
				else:
					print(f"\033[1;31mERRO ao mandar mensagem para {pessoa['nome']}\033[m")
			sleep(5)

	else:
		try:
			pessoas = varrer_group(grupos[int(numero)]["chat_id"])
		except:
			print("\033[1;31mNúmero invalido!\033[m")
			break

		msg = testo()
		print(f"A mensagem sera enviada para {len(pessoas)}")
		print("__"*25)

		for pessoa in pessoas:
			mensagem = send_mensagem(pessoa["id"], msg)
			if mensagem:
				print(f"\033[1;32mMensagem enviada para {pessoa['nome']}\033[m")
				sleep(randint(3, 10))
			else:
				print(f"\033[1;31mERRO ao mandar mensagem para {pessoa['nome']}\033[m")
		sleep(5)
	
	print("=="*25)
