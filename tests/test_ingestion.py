#!/usr/bin/env python

'''
Basic tests for validating and ingesting metadata into mongo
'''

import argparse
import configparser
import json
import os
import pymongo


class TestIngestion:
    """ Test connection, schema, validation, and ingestion. """


    def test_connection_from_filename(self):
        """ Read a config file, connect to MongoDB """

        # TBD: Is secrets file named in config?
        assert(True)


    def test_connection_from_dict(self):
        """ Given a config dict, connect to MongoDB """

        assert(True)


    def test_set_schema(self):
        """ Confirm that schema loads. """

        assert(True)


    def test_set_schema_strictness_loose(self):
        """ Confirm that schema strictness is set to loose. """
     
        assert(True)


    def test_set_schema_strictness_strict(self):
        """ Confirm that schema strictness is set to strict. """

        assert(True)


    def test_validate_loose_passes(self):
        """ Test that doc passes schema validation with loose strictness. """

        assert(True)


    def test_validate_loose_fails(self):
        """ Test that doc fails schema validation with loose strictness. """

        assert(True)


    def test_validate_strict_passes(self):
        """ Test that doc passes schema validation with strict strictness. """

        assert(True)


    def test_validate_strict_fails(self):
        """ Test that doc fails schema validation with strict strictness. """

        assert(True)


    def test_ingestion(self):
        """ Test that doc is ingested successfully. """

        assert(True)


    def test_duplicate_error(self):
        """ Test that duplicate doc error is caught. """

        assert(True)




