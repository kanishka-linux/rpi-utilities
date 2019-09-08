#! /usr/bin/python3

import sys
import time
import subprocess
import sh

def ping_device(addr):
    try:
        out = subprocess.check_output(["sudo", "l2ping", addr, "-c", "1"])
        out = out.decode("utf-8").lower().strip()
    except Exception as err:
        print(err)
        out = "can't connect"
    print(out)
    if "can't connect" in out:
        return False
    else:
        return True

def connect_device(device, addr, counter):
    if ping_device(addr):
        info = device("info", addr)
        print(info)
        if "Connected: no" in info or counter == 0:
            if counter == 0:
                device("disconnect", addr)
                print("disconnect {}".format(addr))
            try:
                device("connect", addr)
                print("connected {}".format(addr))
            except Exception as err:
                print(err)
                counter = -1
        else:
            print("device {} already connected".format(addr))
    else:
        print("device {} is not reachable or switched off".format(addr))
        counter = -1
    return counter

def main():
    device = sh.bluetoothctl
    counter = 0
    while True:
        counter = connect_device(device, sys.argv[1], counter)
        print("counter = {}".format(counter))
        counter += 1
        time.sleep(10)
        
if __name__ == "main":
    main()

