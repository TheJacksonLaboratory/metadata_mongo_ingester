#!/usr/bin/env python

"""
   Provide APIs for connecting to a mongoDB collection, validating docs against a schema,
   and ingesting them
"""

import configparser
import json
import pymongo


class MetadataMongoIngester:

    """
    Provide utilities for ingesting metadata into mongoDB
    
    Has methods to connect to a DB, set a schema, validate docs against a schema, and 
    ingest them.
    """

    def __init__(self):
    """" Initialize data members. """

        self.collection = None

        self.index_keys = None

        self.curr_schema = None

        self.strictness = None


    """
    PUBLIC METHODS
    """


    def ingest_document(self, doc):

        """
        Ingest a document. Validate before ingestion if schema is set.

        Parameters:
            doc (str or dict): If a string is passed, it will be treated as an absolute
            path to a json file containing the metadata to be ingested. If a dict is 
            passed, it will be treated as metadata to be ingested.


       Returns:
           None if successful, or error message string beginning with "Error:".


    def open_connection(self, config_filename):

        """
        Take a user provided configuration and connect to a mongo DB collection.

        Parameters:
            config_filename (str): Absolute path to a config file. Contents of file
            must include:
            1) A key "secrets_file", where the value is an absolute path to secrets file
            2) A key "index_keys", where the value is a key or comma-separated list of
               keys to be used as an index.

        Returns:
            None if successful, or error message string beginning with "Error:".
        """

        return "Error: not yet implemented"




    def set_schema(self, schema_filename=None, strictness="tight"):

        """
        Set or unset the schema file and strictness to be applied during validation.

        Parameters:
            schema_filename (str): Absolute path to json schema file. If None, will clear
            schema. I.e., no schema will be applied.

            strictness (str): Value must be "tight" or "loose". 
                "tight" will require documents to have all fields in the schema, and ONLY 
                those fields.
                "loose" will require documents to have all fields in the schema, but it
                may also have additional fields.

        Returns:
            None if successful, or error message string beginning with "Error:".
        """

        return None


    def validate(self, doc):

        """
        Validate a metadata document. 

        Parameters:
            doc (dict): Metadata document to be validated.

        Returns:
            None if successful, or error message string beginning with "Error:".
        """

        
        
        
    """
    PRIVATE METHODS
    """


     
        

        

    
