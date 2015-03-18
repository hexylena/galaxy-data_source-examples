##Overview

This is a small example for the interaction of Galaxy with an external data source. 

As the external source I chose CherryPy which is a python module for a minimalistic web server. CherryPy takes away some of the work which would be needed starting from SimpleHTTPServer.

###1. Galaxy to CherryPy
In Galaxy the external data source is implemented as a tool with a specific type, namely: *data_source*. A lot of information on data sources can be found on the [Galaxy help pages](https://wiki.galaxyproject.org/Admin/Internals/DataSources).
The main two parameters which are sent from Galaxy to the external data source (EDS) are the *sendToGalaxy* and the *GALAXY_URL* parameters. If *sendToGalaxy* has the value 1 then that should tell the EDS that the incoming traffic is to be sent to a Galaxy instance and not to a normal user. The value of *GALAXY_URL* tells the EDS where to send the result (or where to send a query). On the Galaxy side these parameters have to be set in the xml of the tool file. 

As you can see in the example (cherrypy.xml) the tool goes to the url http://localhost:8090/getdata with the arguments ?sendToGalaxy=1&GALAXY_URL=...localhost:8080... and some others. 


###2. CherryPy to Galaxy
The idea is that the server now provides a form specifically for use within Galaxy. This can be an adapted version of a form provided on the website, it just needs to send the result to Galaxy and add some special parameters. If the results have to be calculated or if providing the results takes some time there is a way to make Galaxy idle and query a specific URL until the results are finished (I didn't test this yet).

1. The cherrypy server getdata function distinguishes between a query coming from a "normal" user and a Galaxy instance.  
2. It provides a form where the action points towards the GALAXY_URL and should have a few (hidden) parameters set
  1. non-hidden length parameter (Galaxy will put this parameter in the final query see point 3)
  2. hidden tool_id which it got from Galaxy
  3. hidden output type, note that you can specify the type however you want. The type is translated by the wrapper to a Galaxy conforming type
  4. hidden URL, this is the URL where Galaxy will send the next/final query (point 3). Again you can name this parameter whatever you want, the xml-wrapper of Galaxy (aka the author of the wrapper) takes care of the translation
  5. you can specify the HTTP method with which Galaxy should query it the result in the last step, if you don't do that the author of the wrapper can specify one (see URL_method in cherrypy.xml) (I have not tested the POST method, I suspect the changes that would have to be made are minimal)

###3. Galaxy to CherryPy
Galaxy will then send the final query back to the CherryPy server. It queries the "generate" method with the length parameter and loads the resulting dataset in the users history. (I suspect if this result is not provided in a reasonable time, this connection will time out and the data insert will fail).