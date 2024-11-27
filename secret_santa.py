import smtplib
from email.message import EmailMessage
import random
import json

def send_email(receiver: str, name: str) -> None:
    textfile = r'path_to_email_content.txt'
    sender = 'sender/yours email'
    password = 'App password' # get from google account

    # Open the plain text file whose name is in textfile for reading.
    with open(textfile) as fp:
        # Create a text/plain message
        content = fp.read()
    content += f'{name}'


    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = f'Enter Subject'
    msg['From'] = sender
    msg['To'] = receiver

    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def select_pairs(email_to_name: dict[str, str]) -> dict[str, str]:
    assigned_pairs = {}
    available_names = set(email_to_name.values())

    for sender_email, sender_name in email_to_name.items():
        potential_receivers = available_names.copy()

        # Avoid pairing someone with themselves
        if sender_name in available_names:
            potential_receivers.remove(sender_name)

        if len(potential_receivers) == 0:
            # If no valid receivers, switch pairs and return
            assigned_pairs[sender_email] = sender_name
            return switch_pair(assigned_pairs)
        else:
            # Randomly select a receiver from the available names
            selected_receiver = random.choice(list(potential_receivers))
            available_names.remove(selected_receiver)
            assigned_pairs[sender_email] = selected_receiver

    return assigned_pairs


def switch_pair(pairs: dict[str, str]) -> dict[str, str]:
    pairs_list = list(pairs.items())
    last_pair = pairs_list.pop()
    last_email, last_assigned_name = last_pair

    # Randomly pick a pair to switch with
    switch_email, switch_name = pairs_list[random.randrange(len(pairs_list))]
    pairs[last_email] = switch_name
    pairs[switch_email] = last_assigned_name

    return pairs

# json in format email : name
with open('json_file.json', encoding='utf-8') as file:
    json_data = json.load(file)


for sender_mail, recipient_name in select_pairs(json_data).items():
    send_email(sender_mail, recipient_name)
