"""
Amazon Dash Button server

Sniff for ARP traffic and detects amazon dash (button) press.
Register events in class Action
"""
import json
import os.path
import requests
from scapy.all import sniff

BUTTONS_FILE_NAME = 'buttons.json'

buttons = {}

NO_SETTINGS_FILE = '''\nNo {} found. \nIf you run application in docker container you
should connect volume with setting files, like
    -v $PWD/amazon-dash-private:/amazon-dash-private:ro'''

def load_buttons():
    """ Load known buttons """
    print('loading buttons')
    if not os.path.isfile(BUTTONS_FILE_NAME):
        print(NO_SETTINGS_FILE.format(BUTTONS_FILE_NAME))
        exit(1)
    with open(BUTTONS_FILE_NAME, 'r', encoding='utf-8-sig') as buttons_file:
        buttons = json.loads(buttons_file.read())
    return buttons

def arp_handler(pkt):
    """ Handles sniffed ARP requests """
    if pkt.haslayer(ARP):
        if pkt[ARP].op == 1: # who-has request
            if pkt[ARP].hwsrc in buttons:
                trigger(buttons[pkt[ARP].hwsrc])
            else:
                print('ARP request from unknown MAC {}'.format(pkt[ARP].hwsrc))

def trigger(button):
    """ Button press action """
    print('button {} pressed'.format(button))
    requests.post('http://localhost:5000/dash/signal/help', data=button)

def main():
    global buttons
    buttons = load_buttons()
    print('amazon_dash started, loaded {} buttons'.format(len(buttons)))
    sniff(prn=arp_handler, filter="arp", store=0)

if __name__ == '__main__':
    main()