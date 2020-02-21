import smtplib
import sys
import os
from configparser import ConfigParser

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

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

def create_attachment(filename):
    attachment = MIMEBase('application', "octet-stream")
    header = 'Content-Disposition', 'attachment; filename="%s"' % filename
    try:
        with open(filename, "rb") as fh:
            data = fh.read()
        attachment.set_payload( data )
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
    except IOError:
        print("Error opening attachment file %s" % filename)
        return None
    return attachment

def send_mail(theme, text, toho, attachments=[]):

    cfg = read_config("config.ini")

    host = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    login = cfg.get("smtp", "login")
    password = cfg.get("smtp", "password")
    from_addr = cfg.get("smtp", "from_addr")

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(toho)
    msg['Subject'] = theme
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    for attachment_file in attachments:
        attachment = create_attachment(attachment_file)
        if attachment is not None:
            msg.attach(attachment)

    server = smtplib.SMTP_SSL(host=host, port=465)
    server.login(login, password)
    server.sendmail(from_addr, toho, msg.as_string())
    server.quit()

if __name__ == "__main__":
    theme = "Hello from andermirik"
    text = "Здесь написано что-то смешное ! ¯\_(ツ)_/¯"

    toho = [
        "andermirik-work@yandex.ua"
    ]

    attachments = [
        "arts/cat.jpg",
        "arts/cat2.png"
    ]

    send_mail(theme, text, toho, attachments)
