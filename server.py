import random
import string
import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"
        
    @cherrypy.expose
    def generate(self, length=8):
        cherrypy.response.headers['Content-Type']= 'text/plain'
        return ''.join(random.sample(string.hexdigits, int(length)))

    @cherrypy.expose
    def getdata(self, sendToGalaxy=0, GALAXY_URL="", hgta_compressType="none", tool_id="none", hgta_outputType="tabular"):
        if int(sendToGalaxy) == 1:
            returnString= """<html>
                      <head></head>
                      <body>
                        <form method="get"
                        """
            returnString += "action=\""+GALAXY_URL+"\">"
            returnString += """
                            <input type="text" value="8" name="length" />
                            <input type="HIDDEN" value="""
            returnString += "\""+tool_id+"\""
            returnString += """name="tool_id">
                            <input type="HIDDEN" value="table" name="outputType">
                            <input type="HIDDEN" value="http://localhost:8090/generate" name="URL">
                            <button type="submit">Send result to galaxy!</button>
                        </form>
                      """
            returnString += "Sending results to Galaxy at: " + GALAXY_URL
            return returnString
        else:
            return "Just returning results. (GALAXY_URL: " + GALAXY_URL + ")"

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8090 })
    cherrypy.quickstart(StringGenerator())
                                             