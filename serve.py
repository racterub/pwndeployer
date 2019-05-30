#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-05-31 00:14:27
# @Author  : Racter (vivi.450@hotmail.com)
# @Profile    : https://racterub.me


import yaml
from argparse import ArgumentParser
import os
import sys

def parseParam():
    parser = ArgumentParser()
    parser.add_argument("path", help="Path to challenges")
    parser.add_argument("port", help="Pwn challenges' serving port (start with this value)")
    parser.add_argument("-t", "--timeout", help="Set timeout limit")
    args = parser.parse_args()
    return args.path, args.port

def checkInput(path, port, time):
    if os.path.isdir(path) and port.isdigit():
        if path[-1] != '/':
            path += '/'
        return True
    else:
        return False

def generateConfig(path, port, timeout):
    base = os.path.dirname(os.path.abspath(__file__)) + "/%s" % path
    chal = [f for f in os.listdir(base)]
    #

if __name__ == "__main__":
    path, port, time = parseParam()
    if checkInput(path, port, time):
        generateConfig(path, port, time)
    else:
        print("Please input the correct value")
        sys.exit(-1)
    # try:
    #     with open('a') as conf:
    #         config = json.load(conf)
    #         run_docker()
    # except FileNotFoundError:
    #     