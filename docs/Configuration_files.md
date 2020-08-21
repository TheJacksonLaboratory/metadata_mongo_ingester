# Configuration files

The user must provide a configuration file containing the details of the mongoDB database and collection. It can be passed to the `open_connection` method via the config_filename parameter, or you can leave that blank, in which case the ingester will by default look in your home directory for a file named `ingester_config.cfg`. The file must contain a section for the development database if you wish to use that, or for the production database if using that instead. The file may contain sections for both. All sections must contain a field named `index_keys` that indicate which field in the metadata will be indexed. Below is an example:
```
[mongodb_dev]
address = ctecho01
authSource = ds_testing
collection = nek_test_new_ingester2
database = ds_testing
index_keys = archived_path
port = 27017
username = ds_testing


[mongodb_prod]
address = ctecho01
authSource = dataservices
collection = archived_metadata
database = dataservices
index_keys = archived_path
port = 27017
username = datasrv

```


# The secrets file
Very similar to the config file, there needs to be a secrets file. It can either be passed to the `open_connection` method via the `secrets_filename` parameter, or left blank, in which case the ingester will look in the user's home directory for a file named `ingester_secrets.cfg`. As above, it must contain a `dev` or `prod` block, or both. For example:
```
[mongodb_dev]
password = 12345678

[mongodb_prod]
password = 87654321
```
NOTE: THESE ARE NOT THE ACTUAL PASSWORDS! Also, each block must have the `password` key, whose value is the *actual* password to the database.


