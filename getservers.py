#!/usr/bin/python
import BeautifulSoup
import urllib
import re
import SourceLib
import time
import socket
import struct 
import psycopg2 
import string
import pywapi

sleeptime = 0.1
conn = psycopg2.connect("dbname=csmeteo user=csmeteo")
cur = conn.cursor()
cur.execute("""set client_encoding to 'latin1'""")

PlayerVector = { 'name' : '', 'time': '', 'kills': '', 'map' : '', 'realtime' : '', 'temperature' : '', 'condition' : '', 'humidity' : '' , 'pressure' : '' }

class AppURLopener(urllib.FancyURLopener):
  ''' Setting right User-Agent '''
  version = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"

def SafeSourceServerQuery(ip,port,value):
  '''Safe source query retrieval with exceptions : returns all server values'''
  global socket
  query = SourceLib.SourceQuery.SourceQuery(ip, int(port))
  value = str(value)
  try:
    returnvalue = query.info()[value]
    return returnvalue 
  except socket.timeout, err:
    print("Could not retrieve value: "+str(err))
  except TypeError, err:
    print("Could not retrieve value: "+str(err))
  except socket.error, err:
    print("Could not retrieve value: "+str(err))
  except struct.error, err:
    print("Could not retrieve value: "+str(err))

def SafeSourceServerPlayersQuery(ip,port):
  '''Safe source query retrieval with exceptions : returns all players'''
  global socket
  query = SourceLib.SourceQuery.SourceQuery(ip, int(port))
  try:
    returnvalue = query.player()
    return returnvalue
  except socket.timeout, err:
    print("Could not retrieve value: "+str(err))
    return 'None'
  except TypeError, err:
    print("Could not retrieve value: "+str(err))
    return 'None'
  except socket.error, err:
    print("Could not retrieve value: "+str(err))
    return 'None'
  except struct.error, err:
    print("Could not retrieve value: "+str(err))
    return 'None'

'''Getting status page source'''
google_result = pywapi.get_weather_from_google('Warsaw,Poland')
yahoo_result = pywapi.get_weather_from_yahoo('PLXX0028', 'metric')
Temperature=google_result['current_conditions']['temp_c']
Condition=google_result['current_conditions']['condition']
Humidity=google_result['current_conditions']['humidity']
Pressure=yahoo_result['atmosphere']['pressure']

urllib._urlopener = AppURLopener()
datasource = urllib.urlopen('http://www.game-monitor.com/search.php?used=10&showEmpty=N&location=PL&num=100&game=cstrike2&vars=sv_password=0&game=cstrike2&location=PL&num=100')
doc = datasource.read()
soup = BeautifulSoup.BeautifulSoup(doc)
attrs={ 'class' : 'sip'}
sips_html = soup.findAll('td', attrs)
sips = re.findall( r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', str(sips_html)) 
for URI in sips:
  print("Address: "+URI)
  RealTime = time.time()
  ip,port = URI.split(':')
  query = SourceLib.SourceQuery.SourceQuery(ip, port)
  MaxPlayers=SafeSourceServerQuery(ip,port,'maxplayers')
  time.sleep(sleeptime)
  NumPlayers=SafeSourceServerQuery(ip,port,'numplayers')
  time.sleep(sleeptime)
  Map=SafeSourceServerQuery(ip,port,'map')
  time.sleep(sleeptime)
  Players=SafeSourceServerPlayersQuery(ip, port)
  print (" `MAP : "+str(Map)+", PLAYERS: "+str(NumPlayers)+"/"+str(MaxPlayers))
  i=0
  while i < len(Players) and Players != 'None':
    i = i+1
    try:
      PlayerVector['name'] = str(Players[i]['name'])
      PlayerVector['time'] = str(Players[i]['time'])
      PlayerVector['kills'] = str(Players[i]['kills'])
      PlayerVector['map'] = str(Map)
      PlayerVector['realtime'] = str(RealTime)
      PlayerVector['temperature'] = str(Temperature)
      PlayerVector['condition'] = str(Condition)
      PlayerVector['humidity'] = str(Humidity)
      PlayerVector['pressure'] = str(Pressure)
      print("Vector : " + str(PlayerVector))
      cur.execute("""INSERT INTO player (name,time,kills,map,realtime,temperature,condition,humidity,pressure) VALUES (%(name)s,%(time)s,%(kills)s,%(map)s,%(realtime)s,%(temperature)s,%(condition)s,%(humidity)s,%(pressure)s)""" ,PlayerVector)
    except IndexError, errormessage:
      print ("Fcuk - didnt add player because :"+str(errormessage))
    except psycopg2.DataError,errormessage:
      print ("Fcuk - didnt add player because :"+str(errormessage))
  conn.commit()

