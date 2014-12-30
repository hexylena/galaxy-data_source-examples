from flask import Flask, request, redirect
app = Flask(__name__)
import urllib
import urllib2
import urlparse
import os
import json

with open('out.json', 'r') as handle:
    data = json.load(handle)

try:
    os.unlink('out.json')
except:
    pass


# We must ping Galaxy with the URL to access the dataset at
#http://GALAXY/async/search/a5mr3ks4j1?STATUS=OK&URL=http://www.data.org/temp/1299292.dat
request_url = data['galaxy'] + urllib.urlencode({'STATUS': 'OK', 'URL': 'http://localhost:4002/data/filename.dat'})
req = urllib2.Request(request_url, data, headers)
urllib2.urlopen(req)

# The data was always available, but now it's "ready"
