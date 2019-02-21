import requests

from . import k8sutils

def createServerUser(user, password, cluster, slicename,config_path):

  serverip = k8sutils.getserverip(slicename,cluster,config_path)

  if serverip == None:
    return None

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




