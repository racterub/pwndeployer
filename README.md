PwnDeployer
===

This is a automatic deployer for pwn challenges in CTF.

Based on docker and xinetd, written in python3

# Usage:
```
usage: serve.py [-h] [-d PATH] [-p PORT] [-i IMAGE] [-t TIME] [-g]

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --dir PATH   Path to challenges
  -p PORT, --port PORT  Pwn challenges' starting port (Default => 6000)
  -i IMAGE, --img IMAGE
                        Docker base image for your pwn challenges (Default =>
                        ubuntu:18.04) or do just do <img>:<tag>
  -t TIME, --timeout TIME
                        Set timeout limit
  -g, --gen-conf        Generate docker-compose.yml
```


see old version at https://github.com/racterub/ctf-pwn-deployer.

