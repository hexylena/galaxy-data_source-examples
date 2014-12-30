# Galaxy Data Source Examples

Simple data source examples to help others building databases which should have Galaxy integration. There are two types of data sources, `sync` and `async`. 

# Synchronous Data Sources

For these data source types, simply requesting a specific URL will provide/generate the data on demand and return it to the requester. For example, providing access to a static file.

Running the example:

1. Install `sync.xml` into your Galaxy toolbox
2. `pip install flask`
3. `python sync.py`
4. Use the tool in Galaxy

# Asynchronous Data Sources

For these, the data must be generated in the background, and Galaxy must be notified of the data source being available by the remote resource.

Running the example:

1. Install `async.xml` into your Galaxy toolbox
2. `pip install flask`
3. `python async.py`
4. Use the tool in Galaxy
5. `python async_finish.py`
