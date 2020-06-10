#!/usr/bin/env python

"""
   Provide APIs for connecting to a mongoDB collection, validating docs against a schema,
   and ingesting them
"""

import configparser
import json
import jsonschema
import os
import pymongo
import re

class MetadataMongoIngester:

    """
    Provide utilities for ingesting metadata into mongoDB
    
    Has methods to connect to a DB, set a schema, validate docs against that schema, and 
    ingest them. Also corrects the archivedPath key if given a wrong one. See help for 
    the __correct_archived_path_key method below.
    """

    def __init__(self):

        """"
        Initialize data members.

        Parameters: None

        Returns: None
        """

        self.collection = None
        self.curr_schema = None
        self.good_path_key = None # Used to correct wrong archivedPath keys
        self.ingester_config = None
        self.path_pattern = None # Used to locate wrong archivedPath keys

        # Metadata docs should have a field named "archived_path" but they may have a 
        # different field that needs to be changed. See comments in the  
        # __correct_archived_path_key method, below.
        self.good_path_key = "archived_path"
        self.path_pattern = re.compile(r'archive.*path', re.IGNORECASE)
        

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
        filename = None
        if type(doc) is str:
            try:
                filename=doc
                with open(filename) as f:
                    doc = json.load(f)
            except Exception as e:
                return f"Error: could not load {filename} as json"

        # Fix the archivedPath key if needed. doc will be an updated document
        # or error message
        doc = self.__correct_archived_path_key(doc)
        if type(doc) is str and doc.startswith("Error"):
            return doc

        # Validation returns None on success, error message otherwise.
        val = self.validate(doc)
        if val:
            return val

        # Use the filename or archivedPath to identify the document for the error message
        if filename:
            id = filename
        else:
            id = doc[self.good_path_key]

        # Attempt ingestion
        try:
            result = self.collection.insert_one(metadata_dict)
            if result.acknowledged:
                return None

        except pymongo.errors.DuplicateKeyError:
            return "Duplicate key, skipped"

        except Exception as e:
            # Use the filename or archivedPath to identify the document for the error message
            if filename:
                id = filename
            else:
                id = doc[self.good_path_key]
            return f"Error: Cannot ingest metadata {id}, received exception {str(e)}."

        return f"Error: Cannot ingest metadata {id}, reason unknown."


    def is_schema_set(self): 

        """
        State whether schema is set.

        Parameters: None

        Returns: bool. True if schema is set, False if not.
        """

        return self.curr_schema is not None


    def open_connection(self, config_filename):

        """
        Take a user provided configuration and connect to a mongo DB collection.

        Parameters:
            config_filename (str): Absolute path to a config file. File must include:
                1) A mongodb section, in brackets. I.e., [mongodb].
                2) A secrets section.
                

        Returns:
            None if successful, or error message string beginning with "Error:".
        """

        # Open config file
        try:
            user_config = configparser.ConfigParser()
            user_config.read(config_filename)
        except Exception as e:
            return f"Error: cannot read config file {config_filename}, received exception {str(e)}."

        # Confirm it has a "mongodb" section
        try:
            mongo_section = user_config["mongodb"]
        except Exception as e:
            return f"Error: no mongodb section in config file {config_filename}."

        # Get the index_keys or return an error if not found.
        if "index_keys" not in mongo_section:
            return f"Error: no index_keys in mongodb section of config file {config_filename}."
        index_key = mongo_section["index_keys"]

        # Get the password from the secrets file or return an error. Must pass the user_config and the
        # directory where the config file is located.
        password = self.__read_secrets_file(user_config, os.path.dirname(config_filename))
        if password.startswith("Error"):
            return password

        # Try to open the connection
        try:
            db_connection = pymongo.MongoClient(mongo_section["address"],
                int(mongo_section["port"]),
                username = mongo_section["username"], password = password,
                authSource = mongo_section["authSource"])
        except Exception as e:
            return f"Error: could not open mongodb connection, received exception {str(e)}."

        # Get the collection from the connection.
        self.collection = db_connection[mongo_section["database"]][mongo_section["collection"]]

        # Create an index if its not already present.
        try:
            self.collection.create_index([(index_key, pymongo.ASCENDING)], unique=True)
        except Exception as e:
            return f"Error: could not create index, received exception {str(e)}."

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
                self.curr_schema = json.load(f)
            # Test that the schema itself is valid by using one of the validators in the
            # jsonschema package. 
            jsonschema.Draft7Validator.check_schema(self.curr_schema)

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
        Correct outdated or wrong archived_path key.

        We want metadata to have a field named 'archived_path', but in some older data it is 
        instead written as 'archiveFolderPath' or 'archivedFolderPath' (note the letter 'd').
        In faculty (derived) data, it might also have a hyphen, incorrect case, or other error. 
        This method will insert the correct key and delete the old one.

        Parameters:
            doc (dict): Metadata document as dict.

        Returns: Updated metadata document as dict.
        """

        # If the metadata has one of the older or incorrect archivedPath keys, change it to the 
        # correct one by copying its value to the correct key and deleting the bad key.

        if self.good_path_key in doc:
            return doc

        for curr_key in doc:
            if (re.match(self.path_pattern, curr_key, re.IGNORECASE) and
                curr_key != self.good_path_key):
                doc[self.good_path_key] = doc[curr_key]
                del doc[curr_key]

        if self.good_path_key not in doc:
            return f"Error: could not find {self.good_path_key} key in document."

        return doc
     
        
    def __read_secrets_file(self, user_config, config_dir):

        """
        Get secrets file from the config, read it, and return the password.

        Parameters:
            user_config (dict): Result of the parsed config file.
            config_dir (str): Absolute path to the directory containing the config file. The secrets
            file is expected to be in this directory also.

        Returns: The password, or an error string beginning with "Error:"
        """

        # Get the secrets filename from the config
        if "secrets" not in user_config:
            return "Error: no secrets section in the config file."

        if "filename" not in user_config["secrets"]:
            return "Error: no filename key in secrets section of the config file."

        secrets_filename = os.path.join(config_dir, user_config["secrets"]["filename"])
        if not os.path.exists(secrets_filename):
            return f"Error: secrets file {secrets_filename} does not exist."

        try:            
            secrets_config = configparser.ConfigParser()
            secrets_config.read(secrets_filename)
        except Exception as e:
            return f"Error: cannot read secrets file {secrets_filename}, received exception {str(e)}."

        try:
            mongo_section = secrets_config["mongodb"]
        except Exception as e:
            return f"Error: no mongodb section in secrets file {secrets_filename}."

        if "password" not in mongo_section:
            return f"Error: no password in secrets file {secrets_filename}."

        password = mongo_section["password"]
        return password
          
        
        

    
