import re

from paypalrestsdk import Invoice
from wufoo import get_wufoo_entries
from gmail_smtp import GmailSmtpSender

ignore_list_path = 'lists\\ignore-list.txt'
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

def clear_entries(entries, include_lists, log_file):
    def determine(entry, include_lists, ignore_lists):
        full_name = entry['Field1'].capitalize().strip().lower() + ' ' + entry['Field2'].capitalize().strip().lower()

        for list_file in ignore_lists:
            with open(list_file, mode='r', encoding='UTF-8') as f:
                ignore_list = read_list(f)
            
                if full_name in ignore_list:
                    return False

        if include_lists is None:
            return True
        else:
            for list_file in include_lists:        
                with open(list_file, mode='r', encoding='UTF-8') as f:
                    include_list = read_list(f)
                
                    if full_name in include_list:
                        return True
        
        return False

    def read_list(f):
        list_raw = str(f.read())
        list_str = re.sub('( |\t)+',' ', list_raw).lower()
        return list_str

    ignore_lists = [ignore_list_path, log_file]
    return [entry for entry in entries if determine(entry, include_lists, ignore_lists)]
        

def send_messages(message_creation_method, title, include_lists, log_file):
    new_entries = clear_entries(get_wufoo_entries(), include_lists, log_file)

    for entry in new_entries:    
        message = message_creation_method(entry['Field1'].strip(), entry['Field19'])
        sender.send_mail(entry['Field9'], title, message, 'kino_logo.png')

        with open(log_file, mode='a', encoding='UTF-8') as f:
            f.writelines(entry['Field1'].capitalize() + ' ' + entry['Field2'].capitalize() + '\n')

if __name__ == "__main__":
    sender = GmailSmtpSender('kinotlvinfo@gmail.com', 'kinotlvinfo3')

    send_messages(create_welcome_message, "KinoTLV Kabaret 2018", None, registration_confirmed_list_path)
    send_messages(create_payment_confirmation_message, "KinoTLV Kabaret 2018 - Participation Confirmed", [paid_list_path], payment_confirmed_list_path)

