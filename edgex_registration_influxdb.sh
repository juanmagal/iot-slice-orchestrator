###
# Register Export Client
###
printf "\n> Registering Export Client\n"

curl http://35.230.159.51:48071/api/v1/registration -X POST -s -S -d @- <<EOF
{
    "name":"InfluxdbPublisher",
    "addressable":{
        "name":"influxdb",
        "address":"35.242.182.28",
        "user":"edgex",
        "password":"edgex",
        "topic":"edgex",
        "port": 8086
    },
    "format":"NOOP",
    "enable":true,
    "destination":"INFLUXDB_ENDPOINT"
}
EOF

