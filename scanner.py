# PINGS ENTIRE IP RANGE OF A NETWORK AND WRITES THE STATISTICS TO A TEXT FILE
#
# Author: Cory Kennedy
#
# Credit: A large portion of this code sourced from Stack Exchange user Thewizy
# https://codereview.stackexchange.com/questions/205285/ip-scanning-program-python-3
#
# Date: 12/1/2018
#
# example execution: "$ python scanner.py 192.168.1 -f ping_log.txt"

import subprocess
import datetime
import re
import argparse
import multiprocessing as mp


def write_result(filename, results):
    with open(filename, "w") as f:
        f.write(f"Start time {datetime.datetime.now()}")
        for ping in results:
            f.write(ping)
        f.write(f"End time {datetime.datetime.now()}")


def ping_subnet(subnet, addr):
    return subprocess.Popen(["ping", f"{subnet}.{addr}", "-c", "1", \
            "-W", "500"], stdout=subprocess.PIPE) \
            .stdout.read() \
            .decode()


def main(subnet, filename):

    pool = mp.Pool(processes=4)

    output = [pool.apply_async(ping_subnet, args=(subnet, addr)) \
            for addr in range(1,255)]

    results = [p.get() for p in output]

    write_result(filename, results)


def parse_arguments():
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <subnet>',
                                     description='ip checker',
                                     epilog="python ipscanner.py 192.168.1 -f somefile.txt")
    parser.add_argument('subnet', type=str, help='the subnet you want to ping')
    parser.add_argument('-f', '--filename', type=str, help='The filename')
    args = parser.parse_args()

    if not re.match(r"(\d{1,3}\.\d{1,3}\.\d{1,3})", args.subnet) \
       or any(a not in range(1, 255) for a in map(int, args.subnet.split("."))):
        parser.error("This is not a valid subnet")

    if " " in args.filename:
        parser.error("The filename cannot contain whitespace")

    return args.subnet, args.filename

if __name__ == '__main__':
    main(*parse_arguments())


