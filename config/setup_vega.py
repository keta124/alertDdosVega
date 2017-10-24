'''
Created on Mar 20, 2017

@author: CrazyDiamond
'''
import requests
import urllib
import smtplib
from elasticsearch import Elasticsearch
import sqlite3
import os

class Es_query(object):
  def __init__(self):
    self.host = '192.168.142.105'
    self.port = 9200

  def query_es(self,index_str, body_dict):
    try:
      es = Elasticsearch([{'host': self.host, 'port': self.port}])
      response = es.search(index=index_str, body=body_dict)
      return response
    except:
      print 'ES QUERY'
      return ""
  def es_dest_ip(self,query):
    try:
      body_ = {
        "size":0,
        "query":{
          "filtered":{
            "query":{
              "query_string":{
                "query":query
              }
            },
            "filter":{
              "range":{
                "@timestamp":{
                  "gte" : "now-300s"
                }
              }
            }
          }
        },
        "aggs":{
          "dest_ip.raw":{
            "terms":{
              "field":"dest_ip.raw",
              "size":5000,
              "order":{
                "_count":"desc"
              }
            }
          }
        }
      }
      index_ = "suricataids-alert-*"
      response=self.query_es(index_, body_)
      return response["aggregations"]["dest_ip.raw"]["buckets"]
    except:
      print 'EXCEPT ES DEST QUERY'
      return []

  def es_src_ip(self,query):
    try:
      body_ = {
        "size":0,
        "query":{
          "filtered":{
            "query":{
              "query_string":{
                "query":query
              }
            },
            "filter":{
              "range":{
                "@timestamp":{
                  "gte" : "now-900s"
                }
              }
            }
          }
        },
        "aggs":{
          "src_ip.raw":{
            "terms":{
              "field":"src_ip.raw",
              "size":50000,
              "order":{
                "_count":"desc"
              }
            }
          }
        }
      }
      index_ = "suricataids-alert-*"
      response= self.query_es(index_, body_)
      return response["aggregations"]["src_ip.raw"]["buckets"]   
    except:
      print 'EXCEPT ES SRC QUERY' 
      return []
class Sms(object):
  def __init__(self,mobile_list,message):
    self.mobile_list = mobile_list
    self.message = message
  def send_sms(self):
    try:
      for mobile in self.mobile_list:
        sms_message=urllib.quote_plus(self.message)
        smsUrl = "http://103.216.121.213:8081/sms/send_sms.php?token=a7b6666333345567abc456767d2dd100345&sdt="+mobile+"&message="+sms_message
        status = requests.request(method="GET", url=smsUrl)
        print status.content
    except:
      print '___EXCEPT SEND SMS___ \n'
class Email(object):
  def __init__(self,list_recipient,message):
    self.list_recipient = list_recipient
    self.message = message    
  def send_gmail(self):
    try:
      gmail_user = "monitorclipvn@gmail.com"
      gmail_pwd = "Rr123456789"
      SUBJECT = "[ATTT] Canh bao server DDOS"
      TEXT = "\nCanh bao server ddos \n\n"+self.message+"\n\n\n\n"
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.login(gmail_user, gmail_pwd)
      BODY = '\r\n'.join([
          'From: ATTT VEGA',
          'Subject: %s' % SUBJECT,
          '', TEXT])
      server.sendmail(gmail_user, self.list_recipient, BODY)
    except:
        print '___EXCEPT SEND MAIL___ \n'
class File_RW(object):
  def __init__(self,file_name,content):
    self.file_name = file_name
    self.content = content
  def writefile(self):
    try:
      path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
      filename_ = path+"/output/"+str(self.file_name)
      print filename_
      if os.path.exists(filename_):
        f= open(filename_, "a+")
      else:
        f= open(filename_, "w")
      lines = f.read().splitlines()
      for content_ in self.content :
        if content_ not in lines:
          linewrite = content_+"\n"
          f.write(linewrite)
      f.close()
    except:
        print "__Except write file__"
class Vega_hostname(object):
  def __init__(self):
      pass
  def find_hostname(self,ip):
    try:
      path = os.path.dirname(os.path.realpath(__file__))
      filename_ = path+"/vegahost.db"
      db = sqlite3.connect(filename_)
      cursor = db.cursor()
      state="SELECT IPAddress, Hostname, Host FROM vega_hostname WHERE IPAddress='"+str(ip)+"'"
      cursor.execute(state)
      all_rows = cursor.fetchall()
      for row in all_rows:
        mess = " "+row[0]+"| "+row[1]+"| "+row[2]
      return mess
    except:
	print 'EXCEPT FIND HOSTNAME'
        return ip_server
