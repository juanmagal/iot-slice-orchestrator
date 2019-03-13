import requests
from requests import ConnectionError

from . import k8sutils


def createServerUser(user, password, cluster, serverip):

  url = 'http://'+serverip+'/users'

  print(url)

  payload = {'email': user , 'password': password }

  try:
    response = requests.post(url, json=payload)
  except ConnectionError as ce:
     return None

  if (response.status_code == 201) or (response.status_code == 200):
     return True
  else:
     print(str(response.status_code))
     print("Error")
     return False

def getToken(payload,serverip):

  url = 'http://'+serverip+'/tokens'

  try:
    response = requests.post(url, json=payload)
  except ConnectionError as ce:
     return None
 
  if (response.status_code == 200) or (response.status_code == 201):
     data = response.json()
     return data['token']
  else:
     return None

def createDevice(serverip,name,user,password):

  payload = {'email': user , 'password': password }

  token = getToken(payload,serverip)

  if token == None:
     return None

  authheader = {'Authorization': token}

  urlthings = 'http://'+serverip+'/things'

  payloaddev = {'type': 'device' , 'name': name }
  
  # Provision device

  try:
    responsedev = requests.post(urlthings, json=payloaddev, headers=authheader)
  except ConnectionError as ce:
     return None

  if responsedev.status_code != 201:
     if responsedev.status_code != 200:
        return None

  locheader = responsedev.headers['Location']

  try:
     devid = locheader[locheader.rindex('/')+1:None]
  except ValueError as ae:
     return None


  urlchan = 'http://'+serverip+'/channels'

  payloadchan = {'name': name}

  try:
    responsechan = requests.post(urlchan, json=payloadchan, headers=authheader)
  except ConnectionError as ce:
     return None

  if responsechan.status_code != 201:
     if responsechan.status_code != 200:
        return None

  locheader = responsechan.headers['Location']

  try:
     chanid = locheader[locheader.rindex('/')+1:None]
  except ValueError as ae:
     return None

  urldevchan= 'http://'+serverip+'/channels/'+chanid+'/things/'+devid

  try:
    responseassocdevtochan = requests.put(urldevchan, headers=authheader)
  except ConnectionError as ce:
     return None

  if responseassocdevtochan.status_code != 201:
     if responseassocdevtochan.status_code != 200:
        return None

  device = getDevice(token,serverip,devid)

  if device == None:
     return None
  
  return {'device': devid, 'channel': chanid, 'key':device.get('key')}


def getDevice(token,serverip,devid):

  authheader = {'Authorization': token}

  url = 'http://'+serverip+'/things/'+devid

  try:
     response = requests.get(url, headers=authheader )
  except ConnectionError as ce:
     return None

  if response.status_code != 200:
     return None
  else:
     data = response.json()
     return data

def deleteDevice(serverip,devid,user,password):

  payload = {'email': user , 'password': password }

  token = getToken(payload,serverip)

  if token == None:
     return False

  authheader = {'Authorization': token}

  urlthings = 'http://'+serverip+'/things/'+devid

  # Delete device
  try:
    responsedev = requests.delete(urlthings, headers=authheader)
  except ConnectionError as ce:
     return None

  if responsedev.status_code != 404:
     if responsedev.status_code != 204:
        if responsedev.status_code != 200:
           return False

  return True
 

