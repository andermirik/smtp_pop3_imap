import poplib, email
import re
from email.parser import Parser
import os
from configparser import ConfigParser
from io import StringIO
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

server = cfg.get("pop3", "server")
port = cfg.get("pop3", "port")
login = cfg.get("pop3", "login")
password = cfg.get("pop3", "password")

server = poplib.POP3_SSL(server, port)

server.user(login)
server.pass_(password)

numMessages = len(server.list()[1])
print("Количество сообщений в ящике:", +numMessages)
for i in range(numMessages):
    print ("\nНомер сообщения: ", i)
    raw_email = b"\n".join(server.retr(i + 1)[1])
    raw_email = raw_email.decode('utf-8')

    parsed_email = email.parser.Parser().parsestr(raw_email)
    Body = []
    sUB = parsed_email['Subject']

    print ("Тема: ", decode(sUB))
    print ("Кому: " + parsed_email['To'])
    f = re.findall(r'[\w\.-]+@[\w\.-]+', (parsed_email['From']))
    #You can print other parameters as weel. Such as attachement, if yes, then you can download the attachment.
    print ("От кого: ", f[0])
    print ("Thread-Index ", parsed_email['Thread-Index'])
    print ("In-Reply-To ", parsed_email['In-Reply-To'])
    print ("Message-ID ", parsed_email['Message-ID'])
    print ("References ", parsed_email['References'])

    resp, lines, octets  = server.retr(i+1)

    print("Сообщение: ", decode(parsed_email.get_payload()))

server.quit()
