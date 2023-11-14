#!/usr/bin/env python
import os
import random
import string
import urllib
from argparse import ArgumentParser
from time import sleep

import requests

parser = ArgumentParser()
parser.add_argument("-g", "--galaxyurl", required=True)
parser.add_argument("-l", "--length", required=True)
args = parser.parse_args()
#print args.galaxyurl

# Simulation of some sophisticated method to generate the data
sleep(5)
data="".join(random.sample(string.hexdigits, int(args.length)))

# Write the file and send the URL to that file back to Galaxy
with open("workfile.tmp",'w+') as f:
    f.write(data)
# Note that the handler is "download" which is defined in the CherryPy file
ans = requests.get(
    args.galaxyurl,
    params={
        "STATUS":"OK",
        "URL":"http://localhost:8090/download?filepath=%s" % os.path.abspath(
            f.name
        )
    }
)

