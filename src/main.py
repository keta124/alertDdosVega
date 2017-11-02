'''
Created on Mar 20, 2017

@author: CrazyDiamond
'''
import sys
import  os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core.detect_cliptv_ddos import *
from core.detect_tcp_ddos import *
from core.detect_udp_ddos import *
import threading
import time

state_cliptv=[0,0,0]
state_tcp=[0,0,0]
state_udp=[0,0,0]
def update_state():
        # List 0 => sms; 1 2 => email
    global state_cliptv
    global state_tcp        
    global state_udp
    while True:
        time.sleep(2000)
        state_cliptv=[0,0,0]
        state_tcp=[0,0,0]
        state_udp=[0,0,0]

def sleep_send_notify():
    try:
        global state_cliptv
        global state_tcp        
        global state_udp
        while True:
            for level in (1,2,3):
                state_udp=alert_udp(level,state_udp)
                state_tcp=alert_tcp(level,state_tcp)
                state_cliptv=alert_cliptv(level,state_cliptv)
                time.sleep(60)
    except:
        print '___ EXCEPT SLEEP SEND EMAIL ___'


if __name__ == '__main__':
    try:
        update_state()
        t = threading.Thread(target=sleep_send_notify, args = ())
        t.start()
        th = threading.Thread(target=update_state, args = ())
        th.start()
    except:
        print 'ERROR MAIN'
