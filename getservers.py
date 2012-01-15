#!/usr/bin/python
#----------+-----------------------------+-----------------------------------------------------
# id       | integer                     | not null default nextval('player_id_seq'::regclass)
# name     | character varying(100)      | 
# time     | timestamp without time zone | not null
# kills    | integer                     | default 0
# map      | character varying(30)       | 
# realtime | timestamp without time zone | not null

import BeautifulSoup
import urllib
import re
import SourceLib
import time
import socket
import struct 
import psycopg2 

sleeptime = 0.05

ServerVector = { 'address' : 'none', 
                 'name' : 'none', 
                 'maxplayers' : 'none',
                 'kills' : 'none',
                 'serverkdratio' : 'none'}
PlayerVector = {}

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
urllib._urlopener = AppURLopener()
status_page = urllib.urlopen('http://www.game-monitor.com/search.php?used=10&showEmpty=N&location=PL&num=100&game=cstrike2&vars=sv_password=0&game=cstrike2&location=PL&num=100')
doc = status_page.read()
soup = BeautifulSoup.BeautifulSoup(doc)
attrs={ 'class' : 'sip'}
sips_html = soup.findAll('td', attrs)
sips = re.findall( r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', str(sips_html)) 
print('Oto aktualnie maksymalnie zaludnione polskie serwery CSa')
for URI in sips:
  print("Address: "+URI)
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
  print ("  `Players:") 
  while i < len(Players) and Players != 'None':
    print('    `-'),
    print("Name:"+str(Players[i]['name']))
    print('       `-'),
    print("kills   : "+str(Players[i]['kills']))
    print("time    : "+str(Players[i]['time']))
    print("kills/s : "+str(Players[i]['kills']/Players[i]['time']))
    i = i+1
    
