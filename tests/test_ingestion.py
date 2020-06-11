#!/usr/bin/env python

'''
Unit tests for ingesting documents
'''

import configparser
import json
import os
from pathlib import Path

from src.MetadataMongoIngester import MetadataMongoIngester


# NOTE: pytest skips classes with constructors, so the test class can't have an 
# __init__ method. But we can initialize things before the class, as shown here.

# Get the directory this script has been called from. Use it to find the root directory 
# for the tests, and confirm the schemas dir and test docs dir is beneath it.
tests_dir = os.path.dirname(os.path.realpath(__file__))
configs_dir = Path(tests_dir, "configs")
schemas_dir = Path(tests_dir, "schemas")
test_docs_dir = Path(tests_dir, "test_docs")
assert Path.is_dir(schemas_dir)
assert Path.is_dir(test_docs_dir)


class TestIngestion:

    """ Test that documents can be ingested. """


    def test_good_doc_file_ingests_with_schema(self):

        """ Given a good schema and a good document as a file, confirm successful ingestion. """
       
        config_filename = os.path.join(configs_dir, "good_config_good_secrets.cfg")
        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.open_connection(config_filename)
        mmi.set_schema(schema_filename)
        doc_filename = os.path.join(test_docs_dir, "good_gt_metadata.json")
        val = mmi.ingest_document(doc_filename)
        assert val == None or val.startswith("Duplicate key")


    def test_good_doc_dict_ingests_with_schema(self):

        """ Given a good schema and a good document as a dict, confirm successful ingestion. """

        config_filename = os.path.join(configs_dir, "good_config_good_secrets.cfg")
        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.open_connection(config_filename)
        mmi.set_schema(schema_filename)
        doc_filename = os.path.join(test_docs_dir, "good_gt_metadata.json")
        with open(doc_filename, 'r') as f:
            doc = json.load(f)
        val = mmi.ingest_document(doc)
        assert val == None or val.startswith("Duplicate key")


    def test_bad_doc_file_ingests_without_schema(self):

        """ Given a bad document (missing a PI) but no schema, confirm successful ingestion. """

        config_filename = os.path.join(configs_dir, "good_config_good_secrets.cfg")
        mmi = MetadataMongoIngester()
        mmi.open_connection(config_filename)
        doc_filename = os.path.join(test_docs_dir, "bad_gt_metadata_missing_PI.json")
        val = mmi.ingest_document(doc_filename)
        assert val == None or val.startswith("Duplicate key")


    def test_bad_doc_no_archived_path_fails(self):

        """ Given a bad document missing an archived path, confirm failed ingestion. """

        config_filename = os.path.join(configs_dir, "good_config_good_secrets.cfg")
        mmi = MetadataMongoIngester()
        mmi.open_connection(config_filename)
        doc_filename = os.path.join(test_docs_dir, "bad_gt_metadata_missing_archived_path.json")
        val = mmi.ingest_document(doc_filename)
        assert val.startswith("Error: no archived_path key")


    def test_archived_path_correction_1(self):

        """ Given a doc with an alternate form of the archived_path key, confirm correction """

        mmi = MetadataMongoIngester()
        doc = { "archivedPath" : "some_path"}
        doc = mmi._MetadataMongoIngester__correct_archived_path_key(doc)       
        assert "archived_path" in doc


    def test_archived_path_correction_2(self):

        """ Given a doc with another alternate form of the archived_path key, confirm correction. """

        mmi = MetadataMongoIngester()
        doc = { "archiveFolderPath" : "some_path"}
        doc = mmi._MetadataMongoIngester__correct_archived_path_key(doc)
        assert "archived_path" in doc





