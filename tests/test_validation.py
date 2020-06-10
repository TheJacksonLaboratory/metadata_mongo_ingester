#!/usr/bin/env python

'''
Unit tests for setting a schema and validating docs against it.
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
schemas_dir = Path(tests_dir, "schemas")
test_docs_dir = Path(tests_dir, "test_docs")
assert Path.is_dir(schemas_dir)
assert Path.is_dir(test_docs_dir)


class TestValidation:

    """ Test that schemas can be set and unset, and that docs can be validated. """

    def test_set_bad_schema_truncated(self):

        """ Given an incorrectly truncated schema file, confirm failure. """

        schema_filename = os.path.join(schemas_dir, "bad_gt-schema_truncated.json")
        val= MetadataMongoIngester().set_schema(schema_filename)
        assert val.startswith("Error: could not set schema")


    def test_set_bad_schema_wrong_data_type(self):

        """ Given a schema file with a wrong data type, confirm failure. """

        schema_filename = os.path.join(schemas_dir, "bad_gt-schema_wrong_data_type.json")
        val= MetadataMongoIngester().set_schema(schema_filename)
        # TBD: This test does not work. 
        assert val.startswith("Error: could not set schema")
        # assert True

    def test_set_good_schema(self):

        """ Given a correct schema file, confirm success. """

        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        val= MetadataMongoIngester().set_schema(schema_filename)
        assert val == None


    def test_set_and_unset_schema(self):

        """ Test that we can set a schema and unset it. """

        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.set_schema(schema_filename)
        assert mmi.is_schema_set() == True
        mmi.set_schema() # Passing no schema file clears the schema
        assert mmi.is_schema_set() == False


    def test_good_doc_file_validates_with_good_schema(self):

        """ Given a good schema and a good document file, confirm successful validation. """

        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.set_schema(schema_filename)
        doc_filename = os.path.join(test_docs_dir, "good_gt_metadata.json")
        val = mmi.validate(doc_filename)
        assert val == None


    def test_good_doc_dict_validates_with_good_schema(self):

        """ Given a good schema and a good document loaded as a dict, confirm successful validation. """

        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.set_schema(schema_filename)
        doc_filename = os.path.join(test_docs_dir, "good_gt_metadata.json")
        with open(doc_filename, 'r') as f:
            doc = json.load(f)
        val = mmi.validate(doc)
        assert val == None


    def test_bad_doc_file_fails_validation_with_good_schema(self):

        """ Given a good schema and a bad document missing a "PI" field, confirm failed validation. """

        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.set_schema(schema_filename)
        doc_filename = os.path.join(test_docs_dir, "bad_gt_metadata_missing_PI.json")
        val = mmi.validate(doc_filename)
        assert val.startswith("Error: document validation failed")


    def test_bad_doc_file_passes_validation_with_unset_schema(self):

        """ Given a bad document missing a "PI" field, set then unset schema, and confirm successful validation. """

        schema_filename = os.path.join(schemas_dir, "good_gt-schema.json")
        mmi = MetadataMongoIngester()
        mmi.set_schema(schema_filename)
        mmi.set_schema()
        doc_filename = os.path.join(test_docs_dir, "bad_gt_metadata_missing_PI.json")
        val = mmi.validate(doc_filename)
        assert val == None




