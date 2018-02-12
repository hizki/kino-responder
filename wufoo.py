import urllib.request as urllib
import json

def get_wufoo_entries():
    base_url = 'https://kinotlv.wufoo.com/api/v3/'
    username = 'GPGI-1IW8-JTEE-OQ3M'
    password = 'kinotlv18'

    password_manager = urllib.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, base_url, username, password)
    handler = urllib.HTTPBasicAuthHandler(password_manager)
    opener = urllib.build_opener(handler)

    urllib.install_opener(opener)

    with urllib.urlopen(base_url+'forms/sbs7wsk0tdxx9t/entries.json?pageSize=100', timeout=120) as response:
        data = response.read()
        decoded_data = data.decode('utf-8')
        entries = json.loads(str(decoded_data))['Entries']

    return entries
