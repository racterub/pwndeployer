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
from subprocess import check_output

def parseParam():
    parser = ArgumentParser()
    parser.add_argument("-d", "--dir", help="Path to challenges", default="chal/", dest="path")
    parser.add_argument("-p", "--port", help="Pwn challenges' starting port (Default => 6000)", type=int, default=6000, dest="port")
    parser.add_argument("-i", "--img", help="Docker base image for your pwn challenges (Default => ubuntu:18.04) or do just do <img>:<tag>", default="ubuntu:18.04", dest="image")
    parser.add_argument("-t", "--timeout", help="Set timeout limit", default=0, dest="time")
    parser.add_argument("-g", "--gen-conf", help="Generate docker-compose.yml", action="store_true", dest="gen_conf")
    parser.add_argument("-e", "--ex-libc", help="Export libc from container", action="store_true", dest="ex_libc")
    args = parser.parse_args()
    return args

def genConf(path, port, image, timeout):
    config = {"services": {}}
    base = os.path.dirname(os.path.abspath(__file__)) + "/%s" % path
    chal = [f for f in os.listdir(base)]
    for i in range(len(chal)):
        baseDir = base + chal[i]
        data = {"build": "chal/%s" % chal[i], "ulimits": {"nproc": 1024}, "ports": ["%d:9999" % port]}
        config['services'][chal[i]] = data
        port += 1
        with open('docker-compose.yml', 'w') as f:
            f.write(yaml.dump({"version": '3'}) + yaml.dump(config))

def exportLibc(path, port, image, timeout):
    base = os.path.dirname(os.path.abspath(__file__)) + "/%s" % path
    chal = [f for f in os.listdir(base)]
    os.mkdir('libc/')
    for i in range(len(chal)):
        os.mkdir("libc/%s" % chal[i])
        containerID = check_output('docker ps -aqf "name=pwndeployer_%s"' % chal[i], shell=True).strip().decode()
        os.system("docker cp --follow-link %s:lib32/libc.so.6 libc/%s/lib32" % (containerID, chal[i]))
        os.system("docker cp --follow-link %s:lib/x86_64-linux-gnu/libc.so.6 libc/%s/lib64" % (containerID, chal[i]))


def setup(path, port, image, timeout):
    config = {"services": {}}
    base = os.path.dirname(os.path.abspath(__file__)) + "/%s" % path
    chal = [f for f in os.listdir(base)]
    for i in range(len(chal)):
        baseDir = base + chal[i]
        os.mkdir(baseDir+"/bin/")
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
            ctfXinetd = setting.read()

        if timeout:
                runsh = '''#!/bin/sh
                exec 2>/dev/null
                timeout %d ./%s''' % (timeout, chal[i])
        else:
            runsh = '''
            #!/bin/sh
            exec 2>/dev/null
            ./%s''' % chal[i]

        shutil.move(baseDir+"/%s" % chal[i], baseDir+'/bin/')
        shutil.move(baseDir+"/flag", baseDir+'/bin/')
        os.chmod(baseDir+'/bin/%s' % chal[i], 0o755)
        with open('start.sh') as f:
            startsh = f.read()

        with open(baseDir+'/start.sh', 'w') as f:
            f.write(startsh)
        with open(baseDir+'/Dockerfile', 'w') as f:
            f.write(dockerfile)
        with open(baseDir+'/bin/run.sh', 'w') as f:
            f.write(runsh)
        with open(baseDir+'/ctf.xinetd', 'w') as f:
            f.write(ctfXinetd)
        data = {"build": "chal/%s" % chal[i], "ulimits": {"nproc": 1024}, "ports": ["%d:9999" % port]}
        config['services'][chal[i]] = data
        port += 1
    with open('docker-compose.yml', 'w') as f:
        f.write(yaml.dump({"version": '3'}) + yaml.dump(config))




if __name__ == "__main__":
    arg = parseParam()
    if os.path.isdir(arg.path):
        if arg.gen_conf:
            genConf(arg.path, arg.port, arg.image, arg.time)
        elif arg.ex_libc:
            exportLibc(arg.path, arg.port, arg.image, arg.time)
        else:
            setup(arg.path, arg.port, arg.image, arg.time)
    else:
        print("Invalid input")
        sys.exit(-1)
