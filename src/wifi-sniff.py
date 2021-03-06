"""
Amazon Dash Button server

Sniff for ARP traffic and detects amazon dash (button) press.
Register events in class Action
"""
from scapy.all import *
import json
import os.path
import requests

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
    if pkt.haslayer(ARP):    # ARP from scapy.all
        if pkt[ARP].op == 1: # who-has request
            if pkt[ARP].hwsrc in buttons:
                trigger(buttons[pkt[ARP].hwsrc])
            else:
                print('ARP request from unknown MAC {}'.format(pkt[ARP].hwsrc))

def trigger(button, retry):
    """ Button press action """
    if not retry:
        print('button {} pressed'.format(button))
    else:
        print('retrying request for button {}'.format(button))
    
    try:
        r = requests.post('http://ec2-34-209-67-178.us-west-2.compute.amazonaws.com:5000/api/v1/dash/signal/help', data=button)
    except requests.exception.Timeout:
        print('request timed out {}'.format(button))
        trigger(button, true)
    except requests.exception.RequestException as e:
        print(e)
        sys.exit(1)

def main():
    global buttons
    buttons = load_buttons()
    print('version 5')
    print('amazon_dash started, loaded {} buttons'.format(len(buttons)))
    sniff(prn=arp_handler, filter="arp", store=0) # sniff from scapy.all

if __name__ == '__main__':
    main()
