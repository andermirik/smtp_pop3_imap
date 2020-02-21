import imaplib, email
import os
from configparser import ConfigParser
import email
import quopri
import base64
def read_config(path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, path)

    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)
    return cfg

def decode(payload):
    l = payload.split('?')
    if len(l) > 2:
        if l[2] == 'Q':
            return quopri.decodestring(l[3]).decode('utf-8')
        if l[2] == 'B':
            return base64.b64decode(l[3]).decode('utf-8')
    return l[0]


cfg = read_config("config.ini")

server = cfg.get("imap", "server")
port = cfg.get("imap", "port")
login = cfg.get("imap", "login")
password = cfg.get("imap", "password")

server = imaplib.IMAP4_SSL(server, port)

server.login(login, password)

server.select()

typ, data = server.search(None, 'ALL') # ищем письма


for num in data[0].split() :
    typ, data = server.fetch(num, '(RFC822)')
    email_message = email.message_from_string(data[0][1].decode('utf-8'))

    print()
    print('Сообщение: ', num.decode('utf-8'))
    print('Тема:', decode(email_message['Subject']))
    print('Кому: ', decode(email_message['To']))
    print('Отправитель: ', decode(email_message['From']))
    print(email_message.get_payload())


server.close()
server.logout()
