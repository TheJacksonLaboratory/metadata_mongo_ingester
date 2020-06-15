# Unit Tests

All unit tests use pytest. There are many online tutorials for pytest, such as [this one](https://www.guru99.com/pytest-tutorial.html).


From either the top level directory, or within the tests directory, simply type `pytest`. Ex:
```
(mmienv) Mon Jun 15 14:25:32 sumner101 /projects/kindln/mmi/metadata_mongo_ingester $ pytest
=========================================================================================== test session starts ===========================================================================================
platform linux -- Python 3.6.7, pytest-5.4.2, py-1.8.1, pluggy-0.13.1
rootdir: /projects/kindln/mmi/metadata_mongo_ingester
collected 22 items

tests/test_connection.py ........                                                                                                                                                                   [ 36%]
tests/test_ingestion.py ......                                                                                                                                                                      [ 63%]
tests/test_validation.py ........                                                                                                                                                                   [100%]

=========================================================================================== 22 passed in 0.73s ============================================================================================
s
```

### What's tested?
[test_connection](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/blob/master/tests/test_connection.py) looks for possible errors in the configuration file and confirms that a connection can be opened.

[test_validation](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/blob/master/tests/test_validation.py) confirms that a schema can be set, validated, and unset, and that only a good document passes validation when a schema is set, but alos that even a document with errors will pass when a schema is not set.

[test_ingestion](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/blob/master/tests/test_ingestion.py) looks for possible errors in a document before attempting to ingest it, and confirms that a properly formatted document is ingested correctly.

