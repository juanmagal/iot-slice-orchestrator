import requests

import json

from . import k8sutils

SERVER_PROTOCOL = "tcp"
SERVER_MQTT_PORT = 1883
SERVER_MQTT_FORMAT = "SENML"

def createExporter(gatewayip,gatewayname,servername,serverip,servertopic,topicuser,topicpassword):

  url = 'http://'+gatewayip+':48071/api/v1/registration'

  registrationdata = {"name":gatewayname,"addressable":addressabledata,"format":SERVER_MQTT_FORMAT,"enable":True,"destination":"MQTT_TOPIC"}
  

  # Provision Exporter

  response = requests.post(url, json=registrationdata)

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True


def deleteExporter(gatewayip,expid):

  url = 'http://'+gatewayip+':48071/api/v1/registration/'+expid

  # Provision Exporter

  response = requests.delete(url)

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True

def createDeviceProfile(gatewayip,devicename,resources):

  url = 'http://'+gatewayip+':48081/api/v1/deviceprofile'
  devpath = "/api/v1/device/{deviceId}/"

  devProfileData = dict()
  devProfileData['name'] = devicename

  # By default we will use Float64 as a type, size 5
  value = {"type": "Float64", "size": "5", "readWrite": "R", "defaultValue": "0", "minimum": "0", "maximum": "500"}
  # By default we will use string and no default unit
  units = { "type": "String", "readWrite": "R", "defaultValue": "" }
  properties = {"value":value,"units":unit} 

  responses = {"code":["200","503"]}
   
  resourceIndex = 0

  for item in resources:
      resourceIndex +=1
      attributes = {"name": item}
      devresdata = {"name": item,"attributes": item, "properties":properties}
      resdata =  {"index": resourceIndex, "operation": "get", "object": item, "parameter": item, "property": "value" }
      getcommandpath = devpath+item
      getcommanddata = {"get":{"path":getcommandpath,"responses":responses}}
      devProfileData['deviceResources'].append(devresdata)
      devProfileData['resources'].append(resdata)
      devProfileData['commands'].append(getcommanddata)

  response = requests.post(url, json=devProfileData)

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True

def createMqttAddressable(gatewayip,devicename):

  url = 'http://'+gatewayip+':48081/api/v1/addressable'

  addressabledata = {"name":devicename, "protocol": "TCP", "address": "0.0.0.0", "port": "1883", "publisher":"CommandPublisher", "user":"admin", "password":"public", "topic":"CommandTopic", "baseURL":"TCP://0.0.0.0:1883", "url":"TCP://0.0.0.0:1883"}



  response = requests.post(url, json=addressabledata)

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True


def createDevice(gatewayip,devicename,protocol,protocolformat,resources):

  if protocol == "MQTT":
     # Created because and addressable is needed, but
     # sending commands to the device will not work for now
     if not createMqttAddressable(gatewayip,devicename):
        return False
  else:
     # No other protocols supported so far
     print("Protocol %s not supported" %protocol)
     return False

  addressable = {"name": devicename}

  createDeviceProfile(gatewayip,devicename,resources)

  profile = {"name": devicename}

  # Only MQTT supported so far
  service = {"name": "edgex-device-mqtt"}

  url = 'http://'+gatewayip+':48081/api/v1/device'

  devicedata = {"name": devicename, "adminState": "UNLOCKED", "operatingState": "ENABLED", "addressable":addressable, "profile":profile, "service":service}

  response = requests.post(url, json=devicedata)

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True
