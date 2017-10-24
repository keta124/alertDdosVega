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
            # udp
            status_wait=alert_udp(level=3,state = state_udp)
            state_udp =status_wait
            time.sleep(5)

            status_wait=alert_udp(level=2,state = state_udp)
            state_udp =status_wait
            time.sleep(5)
                
            status_wait=alert_udp(level=1,state = state_udp)
            state_udp=status_wait
            time.sleep(5)
            
            ### tcp
            status_wait=alert_tcp(level=3,state = state_tcp)
            state_tcp =status_wait
            time.sleep(5)
    
            status_wait=alert_tcp(level=2,state = state_tcp)
            state_tcp =status_wait
            time.sleep(5)
                
            status_wait=alert_tcp(level=1,state = state_tcp)
            state_tcp=status_wait
            time.sleep(5)
            
            ### cliptv
            status_wait=alert_cliptv(level=3,state = state_cliptv)
            state_cliptv =status_wait
            time.sleep(5)
    
            status_wait=alert_cliptv(level=2,state = state_cliptv)
            state_cliptv =status_wait
            time.sleep(5)
                
            status_wait=alert_cliptv(level=1,state = state_cliptv)
            state_cliptv=status_wait
            time.sleep(5)
            print '___ ROTATE  ___ '
            break
    except:
        print '___ EXCEPT SLEEP SEND EMAIL ___'


if __name__ == '__main__':
    try:
        sleep_send_notify()
        #t = threading.Thread(target=sleep_send_notify, args = ())
        #t.start()
        #th = threading.Thread(target=sleep_send_notify, args = ())
        #th.start()
    except:
        print 'ERROR MAIN'
