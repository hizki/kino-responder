import re

from wufoo import get_wufoo_entries

class KinoResponder():
    def __init__(self, ignore_list_path, sender):        
        self.ignore_list_path = ignore_list_path
        self.sender = sender

    def is_entry_needed(self, entry, include_lists, ignore_lists):
        full_name = entry['Field1'].capitalize().strip().lower() + ' ' + entry['Field2'].capitalize().strip().lower()

        if self.lookup_in_lists(full_name, ignore_lists):
            return False

        elif include_lists is None:
            return True
        
        else:
            if self.lookup_in_lists(full_name, include_lists):
                return True
        
        return False

    def lookup_in_lists(self, lookup, list_files):
        for list_file in list_files:        
            with open(list_file, mode='r', encoding='UTF-8') as f:
                list_content = self.read_list(f)
            
                if lookup in list_content:
                    return True

    def read_list(self, f):
        list_raw = str(f.read())
        list_str = re.sub('( |\t)+',' ', list_raw).lower()
        return list_str

    def clear_entries(self, entries, include_lists, log_file):
        ignore_lists = [self.ignore_list_path, log_file]
        return [entry for entry in entries if self.is_entry_needed(entry, include_lists, ignore_lists)]

    def send_messages(self, message_creation_method, title, include_lists, log_file):
        new_entries = self.clear_entries(get_wufoo_entries(), include_lists, log_file)

        for entry in new_entries:    
            message = message_creation_method(entry['Field1'].strip(), entry['Field19'])
            print('Sent this message to {} {}:\n'.format(entry['Field1'], entry['Field2']))
            print(message)
            self.sender.send_mail(entry['Field9'], title, message, 'email-templates\\kino_logo.png')
            

            with open(log_file, mode='a', encoding='UTF-8') as f:
                f.writelines(entry['Field1'].capitalize() + ' ' + entry['Field2'].capitalize() + '\n')
