import requests

from requests import ConnectionError

import json

from . import k8sutils

SERVER_PROTOCOL = "tcp"
SERVER_MQTT_PORT = 1883
SERVER_MQTT_FORMAT = "SENML"

def createExporter(gatewayip,gatewayname,servername,serverip,servertopic,topicuser,topicpassword):

  url = 'http://'+gatewayip+':48071/api/v1/registration'

  addressabledata = {"name":servername+"mqttbroker","protocol":SERVER_PROTOCOL,"address":serverip,"port":SERVER_MQTT_PORT,"publisher":gatewayname,"user":topicuser,"password":topicpassword,"topic":servertopic}

  registrationdata = {"name":gatewayname,"addressable":addressabledata,"format":SERVER_MQTT_FORMAT,"enable":True,"destination":"MQTT_TOPIC"}
  
  # Provision Exporter

  try:
    response = requests.post(url, json=registrationdata)
  except ConnectionError as ce:
     return None

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True


def deleteExporter(gatewayip,gatewayname):

  url = 'http://'+gatewayip+':48071/api/v1/registration/name/'+gatewayname

  # Provision Exporter

  try:
    response = requests.delete(url)
  except ConnectionError as ce:
     return None

  if response.status_code != 200:
     if response.status_code != 204:
        if response.status_code != 404:
         return False

  return True

def createDeviceProfile(gatewayip,devicename,resources):

  url = 'http://'+gatewayip+':48081/api/v1/deviceprofile'
  devpath = "/api/v1/device/{deviceId}/"

  devProfileData = {'name': devicename, 'deviceResources': [], 'resources': [], 'commands': []}

  # By default we will use Float64 as a type, size 5
  value = {"type": "Float64", "size": "5", "readWrite": "R", "defaultValue": "0", "minimum": "0", "maximum": "500"}
  # By default we will use string and no default unit
  units = { "type": "String", "readWrite": "R", "defaultValue": "" }
  properties = {"value":value,"units":units} 

  responses = [{"code":"200","description": "get resource value"},{"code":"503","description": "service unavailable"}]

  resourceIndex = 0

  for item in resources:
      attributes = {"name": item}
      devresdata = {"name": item,"attributes": attributes, "properties":properties}
      resdata =  {"name":item,"get":[{"index": "1", "operation": "get", "object": item, "parameter": item, "property": "value" }]}
      getcommandpath = devpath+item
      getcommanddata = {"name":item,"get":{"path":getcommandpath,"responses":responses}}
      devProfileData['deviceResources'].append(devresdata)
      devProfileData['resources'].append(resdata)
      devProfileData['commands'].append(getcommanddata)

  try:
    response = requests.post(url, json=devProfileData)
  except ConnectionError as ce:
     return None

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True

def deleteDeviceProfile(gatewayip,devicename):

  url = 'http://'+gatewayip+':48081/api/v1/deviceprofile/name/'+devicename

  try:
    response = requests.delete(url)
  except ConnectionError as ce:
     return None

  if response.status_code != 200:
     if response.status_code != 204:
        if response.status_code != 404:
         return False

  return True


def createMqttAddressable(gatewayip,devicename):

  url = 'http://'+gatewayip+':48081/api/v1/addressable'

  addressabledata = {"name":devicename, "protocol": "TCP", "address": "0.0.0.0", "port": 1883, "publisher":"CommandPublisher", "user":"admin", "password":"public", "topic":"CommandTopic", "baseURL":"TCP://0.0.0.0:1883", "url":"TCP://0.0.0.0:1883"}

  try:
    response = requests.post(url, json=addressabledata)
  except ConnectionError as ce:
     return None

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True

def deleteAddressable(gatewayip,devicename):

  url = 'http://'+gatewayip+':48081/api/v1/addressable/name/'+devicename

  try:
    response = requests.delete(url)
  except ConnectionError as ce:
     return None

  if response.status_code != 200:
     if response.status_code != 204:
        if response.status_code != 404:
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

  if not createDeviceProfile(gatewayip,devicename,resources):
     return False

  profile = {"name": devicename}

  # Only MQTT supported so far
  service = {"name": "edgex-device-mqtt"}

  url = 'http://'+gatewayip+':48081/api/v1/device'

  devicedata = {"name": devicename, "adminState": "UNLOCKED", "operatingState": "ENABLED", "addressable":addressable, "profile":profile, "service":service}

  try:
    response = requests.post(url, json=devicedata)
  except ConnectionError as ce:
     return None

  if response.status_code != 201:
     if response.status_code != 200:
        return False

  return True

def deleteDevice(gatewayip,devicename):

  if not deleteAddressable(gatewayip,devicename):
     return False

  if not deleteDeviceProfile(gatewayip,devicename):
     return False

  url = 'http://'+gatewayip+':48081/api/v1/device/name/'+devicename

  try:
    response = requests.delete(url)
  except ConnectionError as ce:
     return None

  if response.status_code != 200:
     if response.status_code != 204:
        if response.status_code != 404:
         return False

  return True

