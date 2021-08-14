import pyautogui as pygu
from time import sleep
import pyperclip
import webbrowser
from datetime import datetime
import httpx
import json
import re

# abrir o navegador
#webbrowser.open_new("https://webwhatsapp.com/")
number_contact = ""
message = ""

# verificar se o qrcode foi registrado
def qrcode ():
    # capturando a posição da tela que se pareça com wp_qrcode.JPG
    wp_qrcode = pygu.locateOnScreen("img/wp_qrcode.JPG", confidence=.8)
    result = 0
    # se alguma posição na tela for encontrada
    if (wp_qrcode):
        print("WP esperando leitura de qrcode")
        result = 1
    return result

def open():
    # verificando se estamos dentro do whats logado
    wp_header = pygu.locateOnScreen("img/wp_header.JPG", confidence=.8)
    if (wp_header):
        print("WP está pronto")
        return 1
    else:
        return 0

def get_number():
    # pegando o número do contato
    result = 0
    wp_lupa = pygu.locateOnScreen("img/wp_lupa.JPG", confidence=.8)
    if (wp_lupa):
        print("WP: Lupa encontrada")
        pygu.moveTo(wp_lupa[0] - 50, wp_lupa[1] + 10, duration=0.5)
        sleep(1)
        pygu.click()
        sleep(1)
        wp_number_detail = pygu.locateOnScreen("img/wp_number_detail.JPG", confidence=.8)
        if (wp_number_detail):
            print("WP: Encontrado detalhes do contato")
            pygu.moveTo(wp_number_detail[0] + 30, wp_number_detail[1] - 70, duration=0.5)
            pygu.tripleClick()
            pygu.hotkey("ctrl", "c")
            sleep(1)
            
            # clicando na conversa
            pygu.moveTo(wp_number_detail[0] - 50, wp_number_detail[1], duration=0.5)
            sleep(1)
            pygu.click()
            
            global number_contact
            number_contact = pyperclip.paste()
            # removendo caracters não númericos
            number_contact = re.sub('[^0-9]', '', number_contact)
            # verificando se existem caracters válidos para um n. de celular
            if (len(number_contact)>=11):
                # removendo o 55 da frente do número
                number_contact = number_contact[2:]
                result = 1

    return result

def new_msg():
    # verificando se existe novas mensagens
    wp_new = pygu.locateOnScreen("img/wp_new.JPG", confidence=.8)
    if (wp_new):
        print("WP: Nova mensagem encontrada")
        pygu.moveTo(wp_new[0], wp_new[1], duration=0.5)
        sleep(1)
        pygu.click()
        return 1
    else:
        return 0

def new_inmessage():
    # verificando se existe uma nova msg dentro da conversa
    wp_inmessage = pygu.locateOnScreen("img/wp_inmessage.JPG", confidence=.8)
    if (wp_inmessage):
        print("Nova mensagem dentro da conversa")
        # movendo para a posição da ultima caixa de texto
        pygu.moveTo(wp_inmessage[0] + 25, wp_inmessage[1], duration=0.5)
        sleep(1)
        # clicar 3 vezes sobre a caixa de texto
        pygu.tripleClick()
        # limpar o clipboard
        pyperclip.copy("")
        # copiar CTRL + C
        pygu.hotkey('ctrl', 'c')
        global message
        message = pyperclip.paste()
        return  1
    else:
        return 0

def get_response():
    global message
    message = message.lower()

    resposta = None
    if ("oi wp" in message):
        resposta = [
            "Olá eu sou WPBOT \n Escolha uma das opções abaixo para que possa ajudar!",
            "*PIADA* para receber uma piada",
            "*DTH* para saber a data e hora atual",
            "*TW* para receber meu canal da twitch"
        ]
    elif ("piada" in message):
        resposta = ["Na minha máquina funciona!"]
    elif ("dth" in message):
        now = datetime.now()
        resposta = ["A data e hora atual é " + str(now.strftime("%d/%m/%Y %H:%M:%S"))]
    elif ("tw" in message):
        resposta = ["Meu canal na twitch é twitch.com/cafecodes"]
    else:
        resposta = None

    return resposta

# def get_api():
#     httpx.get("localhost/")

def send(response):
    # pegando parte por parte do array de resposta
    for msg in response:
        # escevendo a msg
        pygu.typewrite(msg)
        # saltando uma linha
        pygu.hotkey('shift', 'enter')
    sleep(1)
    # enviando a mensagem
    pygu.hotkey('enter')
    return 1

while (1):
    # se qrcode retorna falso
    # passamos da tela de qrcode
    if(qrcode() == False):
        print("Passamos da tela de qrcode")

        # verificando se entramos no whats
        if (open()):
            print("Entramos no whats")

            # verificando se existem novas mensagens
            if (new_inmessage() or new_msg()):

                # verificando se a lupa do header
                # abrindo detalhes e pegando número
                if (get_number()):
                    print("temos o número de contato")

                    # pega a resposta
                    response = get_response()
                    
                    # se a resposta não for nula
                    if (response is not None):

                        # respondendo a msg
                        if (send(response)):
                            print("Respondido")
    sleep(6)
