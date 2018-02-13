#!/usr/bin/python3.5.2

from kino_responder import KinoResponder
from gmail_smtp import GmailSmtpSender

registration_confirmed_list_path = 'lists\\registration-confirmed.txt'
paid_list_path = 'lists\\paid-list.txt'
payment_confirmed_list_path = 'lists\\payment-confirmed.txt'

def create_welcome_message(name, country):
    if country == 'Israel':
        template_file = "email-templates\\israeli-welcome.txt"
    else:
        template_file = "email-templates\\international-welcome.txt"

    return replace_name_in_message(template_file, name)

def create_payment_confirmation_message(name, country):
    if country == 'Israel':
        template_file = 'email-templates\\israeli-payment-confirmation.txt'    
    else:
        template_file = 'email-templates\\international-payment-confirmation.txt'

    return replace_name_in_message(template_file, name)
    
def replace_name_in_message(template_file, name):
    with open(template_file, mode='r') as f:
        template = str((f.read()))
        message = template.replace('<name>', name.capitalize())
        return message

if __name__ == "__main__":
    sender = GmailSmtpSender('kinotlvinfo@gmail.com', 'kinotlvbepita')
    responder = KinoResponder('lists\\ignore-list.txt', sender)
    responder.send_messages(create_welcome_message, "KinoTLV Kabaret 2018", None, registration_confirmed_list_path)
    responder.send_messages(create_payment_confirmation_message, "KinoTLV Kabaret 2018 - Participation Confirmed", [paid_list_path], payment_confirmed_list_path)
