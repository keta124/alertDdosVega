'''
Created on Mar 20, 2017

@author: CrazyDiamond
'''
import os
import time
import sys
from config.setup_vega import *

def alert_tcp(level,state):
    try:
        search_by_dst = "alert.signature:\"VEGA DOS TCP TRACK BY DST LEVEL "+str(level)+"\""
        search_by_src = "alert.signature:\"VEGA DOS TCP TRACK BY SRC\" AND dest_ip:"
        # search es
        es =Es_query()
        list_ip_attacked = es.es_dest_ip(search_by_dst)
        list_server_attacked = []
        hostname_full=""
        ###
        vega_hostname = Vega_hostname()
        if level ==3 :
            for i in range(0,len(list_ip_attacked)):
                if list_ip_attacked[i]["doc_count"] > 5:
                    hostname = vega_hostname.find_hostname(list_ip_attacked[i]["key"])
                    search_by_src_ip=""+search_by_src+"\""+list_ip_attacked[i]["key"]+"\""
                    list_ip_source = es.es_src_ip(search_by_src_ip)
                    ip_source=[]
                    for j in range(0,len(list_ip_source)):
                        ip_source.append(list_ip_source[j]["key"])
                    #### Write file
                    filetxt = str(time.strftime('%Y%m%d_', time.localtime()))+str(list_ip_attacked[i]["key"])+"_tcp_level3.txt"
                    file_w = File_RW(filetxt,ip_source)
                    file_w.writefile()
                    link_http = "http://ids.ovp.vn:8006/"+filetxt+"   (admin/Vega123312##)"
                    hostname_full = hostname +"\n"+"- List source IP blacklist\n"+link_http+ "\n\n"
                    list_server_attacked.append(hostname_full)
                    ### Send Sms
                    if state[0] == 0:
                        sms_message = "DDOS TCP  "+hostname
                        sms = Sms(["0916821333","0936962412"],sms_message)
                        sms.send_sms()
                        state[0] =1
            # Send Email
            if state[1] == 0 and len(list_server_attacked)>0 :
                content_email= "Server critical TCP attack - Level 3 \n\n"+'\r\n'.join(list_server_attacked)
                TO = ['keta124@gmail.com','sontn@vega.com.vn']
                email =Email(TO,content_email)
                email.send_gmail()
                #state[1] =1
            return state
        if level ==2 :
            for i in range(0,len(list_ip_attacked)):
                if list_ip_attacked[i]["doc_count"] > 8:
                    hostname = vega_hostname.find_hostname(list_ip_attacked[i]["key"])
                    search_by_src_ip=""+search_by_src+"\""+list_ip_attacked[i]["key"]+"\""
                    list_ip_source = es.es_src_ip(search_by_src_ip)
                    if len(list_ip_source) >3 :
                        ip_source=[]
                        for j in range(0,len(list_ip_source)):
                            ip_source.append(list_ip_source[j]["key"])
                        #### Write file
                        filetxt = str(time.strftime('%Y%m%d_', time.localtime()))+str(list_ip_attacked[i]["key"])+"_tcp_level2.txt"
                        file_w = File_RW(filetxt,ip_source)
                        file_w.writefile()
                        link_http = "http://ids.ovp.vn:8006/"+filetxt+"   (admin/Vega123312##)"
                        hostname_full = hostname +"\n"+"- List source IP blacklist\n"+link_http+ "\n\n"
                    	list_server_attacked.append(hostname_full)
            # Send Email
            if state[1] == 0 and len(list_server_attacked)>0 :
                content_email= "Server warning TCP attack - Level 2 \n\n"+'\r\n'.join(list_server_attacked)
                TO = ['keta124@gmail.com','sontn@vega.com.vn']
                email =Email(TO,content_email)
                email.send_gmail()
                state[1] =1
            return state
        
        if level ==1 :
            for i in range(0,len(list_ip_attacked)):
                if list_ip_attacked[i]["doc_count"] > 15:
                    hostname = vega_hostname.find_hostname(list_ip_attacked[i]["key"])
                    search_by_src_ip=""+search_by_src+"\""+list_ip_attacked[i]["key"]+"\""
                    list_ip_source = es.es_src_ip(search_by_src_ip)
                    if len(list_ip_source) >-1 :
                        ip_source=[]
                        for j in range(0,len(list_ip_source)):
                            ip_source.append(list_ip_source[j]["key"])
                        filetxt = str(time.strftime('%Y%m%d_', time.localtime()))+str(list_ip_attacked[i]["key"])+"_tcp_level1.txt"
                        file_w = File_RW(filetxt,ip_source)
                        file_w.writefile()
                        link_http = "http://ids.ovp.vn:8006/"+filetxt+"   (admin/Vega123312##)"
                        hostname_full = hostname +"\n"+"- List source IP blacklist\n"+link_http+ "\n\n"
                    	list_server_attacked.append(hostname_full)
            if state[2] == 0 and len(list_server_attacked)>0:
                content_email= "Server maybe TCP attack - Level 1 \n\n"+'\r\n'.join(list_server_attacked)
                TO = ['keta124@gmail.com','sontn@vega.com.vn']
                email =Email(TO,content_email)
                email.send_gmail()
                state[2] =1
            return state
    except:
        print 'EXCEPT DETECT TCP'
        return [1,1,1]
