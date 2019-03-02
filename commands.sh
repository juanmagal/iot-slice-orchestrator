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


iotorch iotgateway create --name=gwtest --cluster=laptop --slice=slicetest --helmpath=helmexamples/helm/edgex-go/
iotorch iotgateway attach --name=gatewaytest --server=servertest
iotorch iotdevice create --name testdevice2 --gateway gwtest --protocol MQTT --resource=temperature --resource=humidity

