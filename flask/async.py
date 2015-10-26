from flask import Flask, request, redirect
app = Flask(__name__)
import urllib
import urlparse
import json

HEAD = "<html><head><title>Async Galaxy Test</title></head><body>"
TAIL = "</body></html>OK"

@app.route("/")
def hello():
    """Index page

    1. Upon choosing the datasource Galaxy performs a HTTP POST request to the
    external datasource's url (specified in the tool configuration file) and passes
    the parameter GALAXY_URL in this request. The value of this parameter contains
    the url where Galaxy will expect the response to be sent at some later time.
    The external site's responsibility is to keep track of this URL as long as the
    user navigates the external site.

    2. As the user navigates the external datasource, it behaves exactly as if
    it would if the request would have not originated from Galaxy
    """

    if 'GALAXY_URL' not in request.args:
        return HEAD + "<h1>Please come here via Galaxy</h1><p>The GALAXY_URL query parameter MUST be set for this to function</p>" + TAIL

    # Normally we would store this in their session data
    gx_url = urllib.urlencode({'gx_url': request.args['GALAXY_URL']})
    # However we aren't developing a big application, so we simply pass it in the URL
    export_url = '/export/?' + gx_url
    # export_url is where the "fun" will happen.
    return HEAD + "<h1>Galaxy Async Data Source Test</h1>" + '<a href="' + export_url + '">Export Data</a>' + get_request_params() + TAIL


def get_request_params():
    """Simply function to display request arguments as a table."""
    result = '<table border=1><thead><tr><th>Key</th><th>Value</th></tr><tbody>'
    for key in request.args:
        result += '<tr><td>%s</td><td>%s</td></tr>' % (key, request.args[key])
    return result + '</tbody></table>'


@app.route("/data/<filename>")
def data(filename):
    return "HELLO\n%s" % filename


@app.route("/fetch/")
def fetch():
    """Route for Galaxy to post the callback URL to

    4. When Galaxy receives the parameters it will run a URL fetching process
    in the background that will resubmit the parameters to the datasource, and
    it will deposit the returned data in the user's account.


    This process operates similarly to the synchronous one, the exception being
    that the datasource will have to later notify Galaxy with the location of
    the data.

    1. The same as steps 1. through 4. for the synchronous data depositing. For
    the step 4 above, Galaxy will create another parameter GALAXY_URL that will
    uniquely characterize the data that is returned. The result of the
    resubmission step of this step is a data entry that is waiting for the data
    source. 1. When the data created by the datasource is ready the datasource
    will have to reconnect to the url specified in GALAXY_URL and submit via
    HTTP GET the STATUS and URL parameters. Galaxy will then make a background
    request to fetch the data stored at the location URL.

    Inter-process communication is performed via a very simple text outputs.
    Commands that have been executed correctly may write any kind of text
    messages. If the text ends with the word OK it will be considered a
    successful submission. Messages that do not end with OK will be treated as
    errors. There is no requirement on interpreting any of the messages; they
    primarily serve for informational/debugging purposes.

    Example Upon returning to the datasource (step 4) Galaxy submits the
    following:

        http://www.data.org/search?value=1&limit=10&gene=HBB1&GALAXY_URL=http://test.g2.bx.psu.edu/async/search/a4mr3ks4j1

    The datasource may then write the following as response:

        received parameters:
        value=1
        limit=10
        gene=HBB1
        GALAXY_URL=http://test.g2.bx.psu.edu/async/search/a4mr3ks4j1
        running query in the background
        closing connection
        OK

    Then, upon a finished data generation this same datasource would make the following request:

        http://test.g2.bx.psu.edu/async/search/a4mr3ks4j1?STATUS=OK&URL=http://www.data.org/temp/1299292.dat

    to which Galaxy could answer:

        Data will be retrieved
        OK
    """
    response = ['received parameters:']
    for key in request.args:
        response.append('%s=%s' % (key, request.args[key]))
    response += ['running query in the background', 'closing connection', 'OK']
    data = {
            'galaxy': request.args['GALAXY_URL']
            }
    with open('out.json', 'w') as handle:
        handle.write(json.dumps(data))
    # At this point the user should run the tool "async_finish.py"
    return '\n'.join(response)

@app.route("/export/")
def export():
    """Return user to Galaxy and provide URL to fetch data from.

    3. At the point where the parameter submission would return data, the external
    datasource will have to instead post these parameters to the url that were sent
    in the GALAXY_URL parameter. Typically this would require that the action
    attribute of the form that generates data to be pointed to the value sent in
    the GALAXY_URL parameter.
    """

    # Extract the Galaxy URL to redirect the user to from the parameters (or any other suitable source like session data)
    return_to_galaxy = request.args['gx_url']
    # Construct the URL to fetch data from. That page should respond with the
    # entire content that you wish to go into a dataset (no
    # partials/paginated/javascript/etc)
    fetch_url = 'http://localhost:4001/fetch/?var=1&b=23'
    # Must provide some parameters to Galaxy
    params = {
            'URL': fetch_url,
            # You can set the dataset type, should be a Galaxy datatype name
            'type': 'tabular',
            # And the output filename
            'name': 'AsyncDataset Name',
            }


    # Found on the web, update an existing URL with possible additional parameters
    url_parts = list(urlparse.urlparse(return_to_galaxy))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    redir = urlparse.urlunparse(url_parts)


    # Then redirect the user to Galaxy
    return redirect(redir, code=302)
    # Galaxy will subsequently make a request to `fetch_url`

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4001, debug=True)
