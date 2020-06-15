Help on module MetadataMongoIngester:

NAME
    MetadataMongoIngester - Provide APIs to validate metadata documents against a schema and ingest them into a MongoDB collection.

CLASSES
    builtins.object
        MetadataMongoIngester
    
    class MetadataMongoIngester(builtins.object)
     |  Provide APIs to validate metadata documents against a schema and ingest them into a MongoDB collection.
     |  
     |  Has methods to connect to a DB, set a schema, validate docs against that schema, and 
     |  ingest them. Also corrects the archivedPath key if given a wrong one. See help for 
     |  the __correct_archived_path_key method below.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      "
     |      Initialize data members.
     |      
     |      Parameters: None
     |      
     |      Returns: None
     |  
     |  get_collection(self)
     |      Get the current collection from the database.
     |      
     |      Parameters: None
     |      
     |      Returns: The mongodb collection named when the connection was opened.
     |  
     |  get_connection(self)
     |      Get the current connection from the database.
     |      
     |      Parameters: None
     |      
     |      Returns: The mongodb connection that was opened.
     |  
     |  ingest_document(self, doc)
     |      Ingest a document. Validate before ingestion if schema is set.
     |      
     |      Parameters:
     |          doc (str or dict):
     |              If dict, metadata document to be ingested.
     |              If str, absolute path to json file containing document.
     |      
     |      Returns:
     |          None if successful, or error message string beginning with "Error:".
     |  
     |  is_schema_set(self)
     |      State whether schema is set.
     |      
     |      Parameters: None
     |      
     |      Returns: bool. True if schema is set, False if not.
     |  
     |  open_connection(self, config_filename)
     |      Take a user provided configuration and connect to a mongo DB collection.
     |      
     |      Parameters:
     |          config_filename (str): Absolute path to a config file. File must include:
     |              1) A mongodb section, in brackets. I.e., [mongodb].
     |              2) A secrets section.
     |              
     |      
     |      Returns:
     |          None if successful, or error message string beginning with "Error:".
     |  
     |  set_schema(self, schema_filename=None)
     |      Set or unset the schema file, insure its validity.
     |      
     |      Parameters:
     |          schema_filename (str): Absolute path to json schema file. If None, will clear
     |          schema. I.e., no schema will be applied.
     |      
     |      
     |      Returns:
     |          None if successful, or error message string beginning with "Error:".
     |  
     |  validate(self, doc)
     |      Validate a metadata document against the current schema. 
     |      
     |      Parameters:
     |          doc (str or dict):
     |              If dict, metadata document to be validated.
     |              If str, absolute path to json file containing document.
     |      
     |      Returns:
     |          None if successful, or error message string beginning with "Error:".
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FILE
    /projects/kindln/mmi/metadata_mongo_ingester/MetadataMongoIngester/MetadataMongoIngester.py


