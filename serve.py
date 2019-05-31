#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-05-31 00:14:27
# @Author  : Racter (vivi.450@hotmail.com)
# @Profile    : https://racterub.me


import yaml
from argparse import ArgumentParser
import os
import sys
import shutil

def parseParam():
    parser = ArgumentParser()
    parser.add_argument("path", help="Path to challenges")
    parser.add_argument("port", help="Pwn challenges' serving port (Default => 6000)", type=int, default=6000)
    parser.add_argument("image", help="Docker base image for your pwn challenges (Default => ubuntu:18.04)", default="ubuntu:18.04")
    parser.add_argument("-t", "--timeout", help="Set timeout limit", default=0, dest="timeout")
    args = parser.parse_args()
    return args.path, args.port, args.image, args.timeout

def setup(path, port, image, timeout):
    config = {"services": {}}
    base = os.path.dirname(os.path.abspath(__file__)) + "/%s" % path
    chal = [f for f in os.listdir(base)]
    for i in range(len(chal)):
        base_dir = base + chal[i]
        os.mkdir(base_dir+"/bin/")
        dockerfile = """FROM %s

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd

RUN useradd -m ctf

COPY ./bin/ /home/ctf/
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh
RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf
RUN chmod 740 /home/ctf/flag

RUN cp -R /lib* /home/ctf
RUN cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev
RUN mknod /home/ctf/dev/null c 1 3
RUN mknod /home/ctf/dev/zero c 1 5
RUN mknod /home/ctf/dev/random c 1 8
RUN mknod /home/ctf/dev/urandom c 1 9
RUN chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin
RUN cp /bin/sh /home/ctf/bin
RUN cp /bin/ls /home/ctf/bin
RUN cp /bin/cat /home/ctf/bin
RUN cp /usr/bin/timeout /home/ctf/bin

WORKDIR /home/ctf

CMD ["/start.sh"]

EXPOSE 9999
""" % image
        with open('xinetd_setting', 'r') as setting:
            ctf_xinetd = setting.read()

        if timeout:
                runsh = '''#!/bin/sh
                exec 2>/dev/null
                timeout %d ./%s''' % (timeout, chal[i])
        else:
            runsh = '''
            #!/bin/sh
            exec 2>/dev/null
            ./%s''' % chal[i]

        shutil.move(base_dir+"/%s" % chal[i], base_dir+'/bin/')
        shutil.move(base_dir+"/flag", base_dir+'/bin/')
        os.chmod(base_dir+'/bin/%s' % chal[i], 0o755)
        with open('start.sh') as f:
            startsh = f.read()

        with open(base_dir+'/start.sh', 'w') as f:
            f.write(startsh)
        with open(base_dir+'/Dockerfile', 'w') as f:
            f.write(dockerfile)
        with open(base_dir+'/bin/run.sh', 'w') as f:
            f.write(runsh)
        with open(base_dir+'/ctf.xinetd', 'w') as f:
            f.write(ctf_xinetd)
        data = {"build": "chal/%s" % chal[i], "ulimit": {"nproc": ["1024:2048"]}, "ports": ["%d:9999" % port]}
        config['services'][chal[i]] = data
        port += 1
    with open('docker-compose.yml', 'w') as f:
        f.write(yaml.dump({"version": 3}) + yaml.dump(config))




if __name__ == "__main__":
    path, port, image, time = parseParam()
    if os.path.isdir(path):
        setup(path, port,image, time)
    else:
        print("Invalid input")
        sys.exit(-1)
    # try:
    #     with open('a') as conf:
    #         config = json.load(conf)
    #         run_docker()
    # except FileNotFoundError:
    #     