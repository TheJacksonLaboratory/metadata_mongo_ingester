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
