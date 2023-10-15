#! /usr/bin/python3

import sys
import sh
import time

def is_volume_lowered(numid):
    out = sh.amixer("cget", "numid={}".format(numid))
    val = int(out.split("\n")[2].strip().split("=")[1].split(',')[0])
    if val < 65536:
        return True
    return False

def set_volume_to_max(numid):
    out = sh.amixer("cset", "numid={}".format(numid), "100%")
    val = int(out.split("\n")[2].strip().split("=")[1].split(',')[0])
    if val == 65536:
        return True
    return False

def main():
    numid = sys.argv[1]
    while True:
        if is_volume_lowered(numid):
            set_volume_to_max(numid)
            print("Volume set to 100%")
        else:
            print("Volume already max")
        time.sleep(2)

if __name__ == "__main__":
    main()
