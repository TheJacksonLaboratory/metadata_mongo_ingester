#!/usr/bin/env python

"""
    Provide APIs to validate metadata documents against a schema and ingest them into a MongoDB collection.   

"""

import configparser
import json
import jsonschema
import os
from pathlib import Path
import pymongo
import re

class MetadataMongoIngester:

    """

    Provide APIs to validate metadata documents against a schema and ingest them into a MongoDB collection.

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
        self.connection = None
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

    
    def get_collection(self):

        """ 

        Get the current collection from the database.

        Parameters: None

        Returns: The mongodb collection named when the connection was opened.

        """

        return self.collection
        

    def get_connection(self):

        """

        Get the current connection from the database.

        Parameters: None

        Returns: The mongodb connection that was opened.

        """

        return self.db_connection
        

    def ingest_document(self, doc):

        """

        Ingest a document. Validate before ingestion if schema is set.

        Note: Documents containing a key with an alternate form of "archived_path",
            such as "archivedPath" or "archivedFolderPath", will be automatically
            corrcted, but documents with no discernable archived_path key will be
            rejected with an error.

        Parameters:
            doc (str or dict):
                If dict, metadata document to be ingested.
                If str, absolute path to json file containing document.

        Returns:
            None if successful, or error message string beginning with "Error:".

        """

        # If given a file, try to open and load it as json.
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
        try:
            val = self.validate(doc)
            if val:
                return f"Could not valiate doc, error was {val}"
        except Exception as e:
            return f"Could not valiate doc, received exception {str(e)}"


        # Attempt ingestion
        try:
            result = self.collection.insert_one(doc)
            if result.acknowledged:
                return None

        except pymongo.errors.DuplicateKeyError:
            return "Duplicate key, skipped"

        except Exception as e:
            return f"Error: Cannot ingest document, received exception {str(e)}."

        return f"Error: Cannot ingest document, reason unknown."


    def is_schema_set(self): 

        """

        State whether schema is set.

        Parameters: None

        Returns: bool. True if schema is set, False if not.

        """

        return self.curr_schema is not None


    def open_connection(self, mode="dev", config_filename=None, secrets_filename=None):

        """

        Take a user provided configuration and connect to a mongo DB collection.

        Parameters:

            mode (str) : Either "dev", "test", or "prod" for development, test, or production

            config_filename (str): Absolute path to a config file. If None, it will look in the
                user's home directory for a file named "ingester_config.cfg".

            secrets_filename (str): Absolute path to a secrets file. If None, it will look in 
                the user's home directory for a file named "ingester_secrets.cfg"

        Returns:
            None if successful, or error message string beginning with "Error:".

        """

        if mode not in ["dev", "test", "prod"]:
            return f"Error: mode must be \"dev\", \"test\", or \"prod\", not \"{mode}\"."

        # Get the configuration from the config file or return an error.
        mongo_section = self.__read_config_file(mode, config_filename)
        if type(mongo_section) == str and mongo_section.startswith("Error"):
            return mongo_section

        # Get the password from the secrets file or return an error.
        password = self.__read_secrets_file(mode, secrets_filename)
        if password.startswith("Error"):
            return password

        # Try to open the connection
        try:
            self.db_connection = pymongo.MongoClient(mongo_section["address"],
                int(mongo_section["port"]),
                username = mongo_section["username"], password = password,
                authSource = mongo_section["authSource"])
        except Exception as e:
            return f"Error: could not open mongodb connection, received exception {str(e)}."

        # Get the collection from the connection.
        self.collection = self.db_connection[mongo_section["database"]][mongo_section["collection"]]

        # Create an index if its not already present.
        try:
            self.collection.create_index([(mongo_section["index_keys"], pymongo.ASCENDING)], unique=True)
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
        This method will insert the correct key and delete the old one. If the document has
        no field for the archived path, an error is returned.

        Parameters:
            doc (dict): Metadata document as dict.

        Returns: Updated metadata document as dict, or string beginning with "Error" if no
            archived_path is found.
        """

        # If the metadata has one of the older or incorrect archivedPath keys, change it to the 
        # correct one by copying its value to the correct key and deleting the bad key.

        if self.good_path_key in doc:
            return doc

        for curr_key in doc:
            if (re.match(self.path_pattern, curr_key) and
                curr_key != self.good_path_key):
                doc[self.good_path_key] = doc[curr_key]
                del doc[curr_key]

        if self.good_path_key not in doc:
            return "Error: no archived_path key in document."

        return doc
     

    def __read_config_file(self, mode, config_filename):

        """

        Read either a given config file or look for one in the user's home directory.

        Parameters:
            config_filename (str) : Absolute path to config file. If None, will look in home dir.

        Returns:
            mongo_config (dict) : dict with config values
            Or
            mongo_config (str) : An error message beginning with "Error"

        """

        # If no config given, use default in user's home directory
        if not config_filename:
            # Use the default config file that should be located in this directory
            src_dir = str(Path.home())
            config_filename = os.path.join(src_dir, "ingester_config.cfg")

        # Open config file
        try:
            user_config = configparser.ConfigParser()
            user_config.read(config_filename)
        except Exception as e:
            return f"Error: cannot read config file {config_filename}, received exception {str(e)}."

        # Confirm it has the rquested dev, test, or prod "mongodb" section
        mode = "mongodb" + '_' + mode
        try:
            mongo_config = user_config[mode]
        except Exception as e:
            return f"Error: no {mode} section in config file {config_filename}."

        # Get the index_keys or return an error if not found.
        if "index_keys" not in mongo_config:
            return f"Error: no index_keys in {mode} section of config file {config_filename}."

        return mongo_config

        
    def __read_secrets_file(self, mode, secrets_filename):

        """

        Read either a given secrets file or look for one in the user's home directory.

        Parameters:
            secrets_filename (str) : Absolute path to config file. If None, will look in home dir.

        Returns:
            password (str) : The password if successful, or an error message beginning with "Error".

        """

        # If no secrets file was given, use the default in the user's home directory
        if not secrets_filename:
            home_dir = str(Path.home())
            secrets_filename = os.path.join(home_dir, "ingester_secrets.cfg")

        if not os.path.exists(secrets_filename):
            return f"Error: secrets file {secrets_filename} does not exist."

        try:
            secrets_config = configparser.ConfigParser()
            secrets_config.read(secrets_filename)
        except Exception as e:
            return f"Error: cannot read secrets file {secrets_filename}, received exception {str(e)}."

        # Build the tag of the desired section
        mode = "mongodb" + '_' + mode
        try:
            mongo_section = secrets_config[mode]
        except Exception as e:
            return f"Error: no {mode} section in secrets file {secrets_filename}."

        if "password" not in mongo_section:
            return f"Error: no password in secrets file {secrets_filename}."

        password = mongo_section["password"]
        return password
      
        
        

    
