# MetadataMongoIngester
    Provide APIs to validate metadata documents against a schema and ingest them into a MongoDB collection.

   

## Overview
   
   
### Usage
All methods are detailed on the [methods](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/blob/master/docs/methods.md) page.

Open a connection by providing a [configuration file](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/blob/master/docs/Configuration_files.md) to the ingester's `open_connection` method.

Set, validate, or unset a schema with the ingester's `set_schema` method. 

Validate a document against a schema with the `validate` method.

Ingest a document with the `ingest_document` method. Please see the note in this method's help regarding the required `archived_path` field.


### Unit Tests
The [Unit tests](https://github.com/TheJacksonLaboratory/metadata_mongo_ingester/blob/master/docs/Unit_tests.md) details the structure and purpose of the unit test files. 

## Questions?
Please contact [Neil Kindlon](mailto:Neil.Kindlon@jax.org) or [Mitch Kosta](mailto:Mitch.Kosta@jax.org) in the [Research IT](https://jacksonlaboratory.sharepoint.com/sites/ResearchIT) department for assistance.
