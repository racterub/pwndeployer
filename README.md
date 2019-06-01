PwnDeployer
===

This is a automatic deployer for pwn challenges in CTF.

Based on docker and xinetd, written in python3

# Usage: 
```
usage: serve.py [-h] [-t TIMEOUT] path port image

positional arguments:
  path                  Path to challenges
  port                  Pwn challenges' serving port (Default => 6000)
  image                 Docker base image for your pwn challenges (Default =>
                        ubuntu:18.04)

optional arguments:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        Set timeout limit
```

# Example
`./serve.py chal/ 9000 ubuntu:16.04`
`docker-compose up`


see old version at https://github.com/racterub/ctf-pwn-deployer.

