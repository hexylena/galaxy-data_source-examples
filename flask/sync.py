from future import standard_library
standard_library.install_aliases()
from flask import Flask, request, redirect
app = Flask(__name__)
import urllib.request, urllib.parse, urllib.error
import urllib.parse

HEAD = "<html><head><title>Sync Galaxy Test</title></head><body>"
TAIL = "</body></html>"

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

    # Normally we would store this in their session data
    gx_url = urllib.parse.urlencode({'gx_url': request.args['GALAXY_URL']})
    # However we aren't developing a big application, so we simply pass it in the URL
    export_url = '/export/?' + gx_url
    # export_url is where the "fun" will happen.
    return HEAD + "<h1>Galaxy Sync Data Source Test</h1>" + '<a href="' + export_url + '">Export Data</a>' + get_request_params() + TAIL


def get_request_params():
    """Simply function to display request arguments as a table."""
    result = '<table border=1><thead><tr><th>Key</th><th>Value</th></tr><tbody>'
    for key in request.args:
        result += '<tr><td>%s</td><td>%s</td></tr>' % (key, request.args[key])
    return result + '</tbody></table>'

@app.route("/fetch/")
def fetch():
    """Route for Galaxy to fetch data at

    4. When Galaxy receives the parameters it will run a URL fetching process
    in the background that will resubmit the parameters to the datasource, and it
    will deposit the returned data in the user's account.
    """

    response = ['#Key\tValue']
    for key in request.args:
        response.append('%s\t%s' % (key, request.args[key]))
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
    fetch_url = 'http://localhost:4000/fetch/?var=1&b=23'
    # Must provide some parameters to Galaxy
    params = {
            'URL': fetch_url,
            # You can set the dataset type, should be a Galaxy datatype name
            'type': 'tabular',
            # And the output filename
            'name': 'SyncDataset Name',
            }


    # Found on the web, update an existing URL with possible additional parameters
    url_parts = list(urllib.parse.urlparse(return_to_galaxy))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    redir = urllib.parse.urlunparse(url_parts)


    # Then redirect the user to Galaxy
    return redirect(redir, code=302)
    # Galaxy will subsequently make a request to `fetch_url`

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
