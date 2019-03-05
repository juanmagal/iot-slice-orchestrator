# Clusters
iotorch k8scluster create --name=laptop --ip=192.168.122.150 --k8shelmport=44134 --k8scontext=laptop
iotorch k8scluster create --name=pc --ip=192.168.1.105 --k8shelmport=44134 --k8scontext=pc
iotorch k8scluster create --name=rpi --ip=192.168.1.160 --k8shelmport=44134 --k8scontext=rpi

# Slices
iotorch iotslice create --name=slice1 --edge pc --cloud pc
iotorch iotslice create --name=slice2 --edge laptop --cloud pc
iotorch iotslice create --name=slice3 --edge rpi --cloud pc

# Servers
iotorch iotserver create --name iotserver1 --cluster=pc --slice=slice1 --helmpath=./helmexamples/helm/mainflux/
iotorch iotserver create --name iotserver2 --cluster=pc --slice=slice2 --helmpath=./helmexamples/helm/mainflux/
iotorch iotserver create --name iotserver3 --cluster=pc --slice=slice3 --helmpath=./helmexamples/helm/mainflux/

iotorch iotserver set --name=iotserver1 --user=testuser@test.com --password=123456
iotorch iotserver set --name=iotserver2 --user=testuser@test.com --password=123456
iotorch iotserver set --name=iotserver3 --user=testuser@test.com --password=123456

# Gateways
iotorch iotgateway create --name=iotgw1 --cluster=pc --slice=slice1 --helmpath=helmexamples/helm/edgex-go/
iotorch iotgateway create --name=iotgw2 --cluster=laptop --slice=slice2 --helmpath=helmexamples/helm/edgex-go/
iotorch iotgateway create --name=gwtest --cluster=rpi --slice=slice3 --helmpath=helmexamples/helm-arm/edgex-go/
 
iotorch iotgateway attach --name=iotgw1 --server=iotserver1
iotorch iotgateway attach --name=iotgw2 --server=iotserver2
iotorch iotgateway attach --name=iotgw3 --server=iotserver3


# Devices

iotorch iotdevice create --name=iotdevice1 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice2 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice3 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice4 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice5 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice6 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice7 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice8 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice9 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice10 --gateway iotgw1 --protocol MQTT --resource=temperature --resource=humidity

iotorch iotdevice create --name=slice2iotdevice1 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice2 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice3 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice4 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice5 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice6 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice7 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice8 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice9 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=slice2iotdevice0 --gateway iotgw2 --protocol MQTT --resource=temperature --resource=humidity

iotorch iotdevice create --name=iotdevice1 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice2 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice3 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice4 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice5 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice6 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice7 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice8 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice9 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity
iotorch iotdevice create --name=iotdevice10 --gateway iotgw3 --protocol MQTT --resource=temperature --resource=humidity


