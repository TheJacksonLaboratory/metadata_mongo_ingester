# Configuration files

The user must provide a configuration file containing the details of the mongoDB database and collection, as well as the name of the secrets file that has the password to the database. An example is shown below.

```
[mongodb]
address = server_name
authSource = user_credentials_db_name
collection = metadata_ingester_tests_config
database = db_name
index_keys = archived_path
port = port_num
username = db_account_username

[secrets]
filename = dev_secrets.cfg
```

Both the `[mongodb]` and `[secrets]` sections are required. Each must have all of the keys shown above. The values shown above are place holders. If you are unsure what actual values to use, please see a member of Research IT for assistance.



# The secrets file
The secrets file named in the `[secrets]` section of the config file **must appear in the same directory** as the configuration file. An example secrets file is shown below.

```
[mongodb]
password = 12345678
```

The `[mongodb]` section is required. It must have the `password` key, whose value is the actual password to the database.


