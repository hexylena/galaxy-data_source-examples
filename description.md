##Overview

This is a small example for the interaction of Galaxy with an external data source. 

As the external source I chose CherryPy which is a python module for a minimalistic web server. CherryPy takes away some of the work which would be needed starting from SimpleHTTPServer.

###1. Galaxy to CherryPy
In Galaxy the external data source is implemented as a tool with a specific type, namely: *data_source*. A lot of information on data sources can be found on the [Galaxy help pages](https://wiki.galaxyproject.org/Admin/Internals/DataSources).
The main two parameters which are sent from Galaxy to the external data source (EDS) are the *sendToGalaxy* and the *GALAXY_URL* parameters. If *sendToGalaxy* has the value 1 then that should tell the EDS that the incoming traffic is to be sent to a Galaxy instance and not to a normal user. The value of *GALAXY_URL* tells the EDS where to send the result (or where to send a query). On the Galaxy side these parameters have to be set in the xml of the tool file. 

As you can see in the example (cherrypy.xml) the tool goes to the url http://localhost:8090/getdata with the arguments ?sendToGalaxy=1&GALAXY_URL=...localhost:8080... and some others. 


###2. CherryPy to Galaxy
1. The cherrypy server getdata function distinguishes between a query coming from a "normal" user and a Galaxy instance.  
2. It provides a form where the action points towards the GALAXY_URL 
  1. huhu
  2. spencer