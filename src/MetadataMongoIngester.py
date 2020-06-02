#!/usr/bin/env python

"""
   Provide APIs for connecting to a mongoDB collection, validating docs against a schema,
   and ingesting them
"""

import configparser
import json
import jsonschema
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
        self.ingester_config = None
        self.curr_schema = None
        self.good_path_key = None # Used to correct wrong archivedPath keys
        self.index_keys = None
        self.path_pattern = None # Used to locate wrong archivedPath keys

        self.ingester_config = configparser.ConfigParser()
        self.ingester_config.read()
        self.good_path_key = self.ingester_config[fix_archived_path]["good_key"]
        self.path_pattern = self.ingester_config[fix_archived_path][path_pattern]
        


    """
    PUBLIC METHODS
    """


    def ingest_document(self, doc):

        """
        Ingest a document. Validate before ingestion if schema is set.

        Parameters:
            doc (str or dict):
                If dict, metadata document to be ingested.
                If str, absolute path to json file containing document.

        Returns:
            None if successful, or error message string beginning with "Error:".
        """

        # Try to open and load json file
        if type(doc) is str:
            try:
                filename=doc
                with open(filename) as f:
                    doc = json.load(f)
            except Exception as e:
                return f"Error: could not load {filename} as json"

        # Validation returns None on success, error message otherwise.
        val = self.validate(doc)
        if val:
            return val

        # Fix the archivedPath key if needed
        doc = self.__correct_archived_path_key(doc)

        #TBD: still needs actual ingestion        

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

        

        return None



    def set_schema(self, schema_filename=None):

        """
        Set or unset the schema file, insure its validity.

        Parameters:
            schema_filename (str): Absolute path to json schema file. If None, will clear
            schema. I.e., no schema will be applied.


        Returns:
            None if successful, or error message string beginning with "Error:".
        """


        # Clear schema if given an empty filename.
        if not schema_filename:
            self.curr_schema = None
            return None

        # Attempt to load the schema file as JSON and validate it.
        try:
            with open(schema_filename, 'r') as f:
                self.curr_schema = json.loads(f)
            # Test that the schema itself is valid by using one of the validators in the
            # jsonschema package. 
            jsonschema.Draft3Validator.check_schema(self.curr_schema)

        except Exception as e:
            return f"Error: could not set schema {schema_filename}, received exception {str(e)}." 

        return None


    def validate(self, doc):

        """
        Validate a metadata document against the current schema. 

        Parameters:
            doc (str or dict):
                If dict, metadata document to be validated.
                If str, absolute path to json file containing document.

        Returns:
            None if successful, or error message string beginning with "Error:".
        """

        # If no schema is currently set, there's nothing to do.
        if not self.curr_schema:
            return None

        if type(doc) not in [str, dict]:
            return f"Error: doc must be a str or dict"

        # Try to open and load json file
        if type(doc) is str:      
            try:
                filename=doc
                with open(filename) as f:
                    doc = json.load(f)
            except Exception as e:
                return f"Error: could not load {filename} as json"

        # Attempt to validate doc against shcema
        try:
            jsonschema.validate(instance=doc, schema=self.curr_schema)
        except Exception as e:
            return f"Error: document validation failed, received exception {str(e)}"

        return None     
    
    """
    PRIVATE METHODS
    """


    def __correct_archived_path_key(self, doc): 

        """
        Correct outdated or wrong archivedPath key.

        We want metadata to have a field named 'archivedPath', but in some older data it is 
        instead written as 'archiveFolderPath' or 'archivedFolderPath' (note the letter 'd').
        In faculty(derived) data, it might also have an underscore or incorrect case.

        Parameters:
            doc (dict): Metadata document as dict.

        Returns: Updated metadata document as dict.
        """

        # If the metadata has one of the older or incorrect archivedPath keys, change it to the 
        # correct one by copying its value to the correct key and deleting the bad key.

        for curr_key in doc:
            if (re.match(self.path_pattern, curr_key, re.IGNORECASE) and
                curr_key != self.good_path_key):
                doc[self.good_path_key] = doc[curr_key]
                del doc[curr_key]
        return doc
     
        

        

    
