import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import urllib.parse
import os
import json

with open("out.json", "r") as handle:
    data = json.load(handle)

# We must ping Galaxy with the URL to access the dataset at
# http://GALAXY/async/search/a5mr3ks4j1?STATUS=OK&URL=http://www.data.org/temp/1299292.dat
request_url = (
    data["galaxy"]
    + "?"
    + urllib.parse.urlencode(
        {"STATUS": "OK", "URL": "http://localhost:4001/data/filename.dat"}
    )
)
req = urllib.request.Request(request_url)
urllib.request.urlopen(req)

# The data was always available, but now it's "ready"
