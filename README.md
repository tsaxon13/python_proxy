This runs a web service that you will be able to use to set up a tunnel through the hosting
machine to a port on a remote machine.

# Running

python server.py [port]

`
$ python server.py
http://0.0.0.0:8080/
`

or running with a specific port

`
$ python server.py
http://0.0.0.0:8000/
`

# Usage

http://<hostname or IP of server>:<port>/proxysetup?ip=<target ip>&port=<target port>

`
$ curl -G "http://bast.verizon.net:8080/proxysetup" --data-urlencode "ip=192.168.1.58" --data-urlencode "port=22"
Connect to bast.verizon.net on port 44616
`
