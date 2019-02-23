import requests

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

