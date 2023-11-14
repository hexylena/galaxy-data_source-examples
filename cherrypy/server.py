import string
import random
import cherrypy
import urllib
import os
import requests
import subprocess
from cherrypy.lib.static import serve_file


class StringGenerator(object):

    # Default behaviour
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    # This method generates the data "on the fly" such that Galaxy can retrieve it immediately
    # for synchronous communication 
    @cherrypy.expose
    def generate(self, length=2, **params):
        cherrypy.response.headers['Content-Type']= 'text/plain'
        return ''.join(random.sample(string.hexdigits, int(length)))
        
    # The method necessary for the exchange of data with Galaxy synchronously
    @cherrypy.expose
    def getdata(self, sendToGalaxy=0, GALAXY_URL="", hgta_compressType="none", tool_id="none", hgta_outputType="tabular"):
        if int(sendToGalaxy) == 1:
            print("Tool_id: " + tool_id)
            returnString= """<html>
                      <head></head>
                      <body>
                        <form method="get"
                        """
            returnString += " action=\""+GALAXY_URL+"\">"
            returnString += """
                            <input type="text" value="8" name="length" />
                            <input type="HIDDEN" value="""
            returnString += "\""+tool_id+"\""
            # Note the URL parameter, this is where we tell Galaxy to get the data from
            returnString += """ name="tool_id">
                            <input type="HIDDEN" value="table" name="outputType">
                            <input type="HIDDEN" value="http://localhost:8090/generate" name="URL">
                            <button type="submit">Send result to galaxy!</button>
                        </form>
                        """
            returnString += "Sending results to Galaxy at: " + GALAXY_URL
            return returnString
        else:
            return "Just returning results. (GALAXY_URL: " + GALAXY_URL + ")"
            
    # The method necessary for the exchange of data with Galaxy asynchronously
    @cherrypy.expose
    def getdata_async(self, length=8, sendToGalaxy=0, GALAXY_URL="", hgta_compressType="none", tool_id="none", hgta_outputType="tabular", data_id=-1, outputType="table"):
        # if a data_id is sent by Galaxy we know that the Galaxy URL is the final adress 
        # where the results should be sent to
        if int(data_id) != -1:
            # we need to fork here and generate the data
            # remembering the Galaxy_url 
            subprocess.Popen(["python", "generate_data_async.py", "-g" ,str(GALAXY_URL) , "-l" , str(length)] )
            # we answer OK to this GET and Galaxy will start continuously checking 
            # if we sent the results yet
            return "OK"

        # this handles the initial request by Galaxy
        # like in the synchronous case here we specify hidden parameters 
        # Note the lack of the "URL" parameter, this makes it necessary
        # that "getdata_async" handles both the initial request and the second
        # request which sends a data_id
        # ... Maybe this will be fixed/changed ...
        elif int(sendToGalaxy) == 1:
            returnString= """<html>
                      <head></head>
                      <body>
                        <form method="get"
                        """
            returnString += "action=\""+GALAXY_URL+"\">"
            returnString += """
                            <input type="HIDDEN" value="""
            returnString += "\""+tool_id+"\""
            returnString += """ name="tool_id">
                            <input type="text" value="8" name="length" />
                            <input type="HIDDEN" value="table" name="outputType">
                            <button type="submit">Send result to galaxy!</button>
                        </form>
                        """
            returnString += "Sending results to Galaxy at: " + GALAXY_URL
            return returnString
        # Not coming from Galaxy
        else:
            return "Just returning results. (GALAXY_URL: " + GALAXY_URL + ")"

    # Function necessary for the download of target data which
    # takes some time to retrieve
    @cherrypy.expose
    def download(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")
            
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8090 })
    cherrypy.quickstart(StringGenerator())
