# Galaxy Data Source Examples

Simple data source examples to help others building databases which should have Galaxy integration. There are two types of data sources, `sync` and `async`. 

# Synchronous Data Sources

For these data source types, simply requesting a specific URL will provide/generate the data on demand and return it to the requester. For example, providing access to a static file.

Running the example:

1. Copy `sync.xml` to `$GALAXY_ROOT/tools/data_source/`
2. Add it to your `$GALAXY_ROOT/config/tool_conf.xml`
3. `pip install flask`
4. `python sync.py`
5. Use the tool in Galaxy

# Asynchronous Data Sources

For these, the data must be generated in the background, and Galaxy must be notified of the data source being available by the remote resource.

Running the example:

1. Copy `async.xml` to `$GALAXY_ROOT/tools/data_source/`
2. Add it to your `$GALAXY_ROOT/config/tool_conf.xml`
3. `pip install flask`
4. `python async.py`
5. Use the tool in Galaxy
6. `python async_finish.py`


# Notes

- http://dev.list.galaxyproject.org/tool-type-quot-data-source-async-quot-td4260262.html
- http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3092608/
- https://wiki.galaxyproject.org/Admin/Internals/DataSources
