import requests

from . import k8sutils


def createServerUser(user, password, cluster, serverip):

  url = 'http://'+serverip+'/users'

  payload = {'email': user , 'password': password }

  response = requests.post(url, json=payload)

  if (response.status_code == 201) or (response.status_code == 200):
     return getToken(payload,serverip)
  else:
     return None

def getToken(payload,serverip):

  url = 'http://'+serverip+'/tokens'

  response = requests.post(url, json=payload)
 
  if response.status_code == 200:
     return None
  else:
     data = response.json()
     return data['token']

def createDevice(token, serverip,name):

  authheader = {'Authorization': token}

  urlthings = 'http://'+serverip+'/things'

  payloaddev = {'type': 'device' , 'name': name }
  
  # Provision device

  responsedev = requests.post(urlthings, json=payloaddev, headers=authheader)

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

  responsechan = requests.post(urlchan, json=payloadchan, headers=authheader)

  if responsechan.status_code != 201:
     if responsechan.status_code != 200:
        return None

  locheader = responsechan.headers['Location']

  try:
     chanid = locheader[locheader.rindex('/')+1:None]
  except ValueError as ae:
     return None

  urldevchan= 'http://'+serverip+'/channels/'+chanid+'/things/'+devid

  responseassocdevtochan = requests.put(urldevchan, headers=authheader)

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

  response = requests.get(url, headers=authheader )

  if response.status_code != 200:
     return None
  else:
     data = response.json()
     return data

def deleteDevice(token,serverip,devid):

  authheader = {'Authorization': token}

  urlthings = 'http://'+serverip+'/things/'+devid

  # Delete device

  responsedev = requests.delete(urlthings, headers=authheader)

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True
 

