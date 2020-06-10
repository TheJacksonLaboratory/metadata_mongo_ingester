#!/usr/bin/env python

'''
Unit tests for parsing the config file needed to open a mongodb connection
'''

import configparser
import os
from pathlib import Path

from src.MetadataMongoIngester import MetadataMongoIngester


# NOTE: pytest skips classes with constructors, so the test class can't have an 
# __init__ method. But we can initialize things before the class, as shown here.

# Get the directory this script has been called from. Use it to find the root directory 
# for the tests, and confirm the configs dir is beneath it.
tests_dir = os.path.dirname(os.path.realpath(__file__))
configs_dir = Path(tests_dir, "configs")
assert Path.is_dir(configs_dir)


class TestConnection:

    """ Test that config files are required to have correct fields and format """

    def test_bad_config_bad_format(self):

        """ Given a poorly formatted config file, confirm failure. """

        config_filename = os.path.join(configs_dir, "bad_config_format.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: cannot read config file")


    def test_bad_config_no_mongodb_section(self):

        """ Given a config file missing a mongodb section, confirm failure. """

        config_filename = os.path.join(configs_dir, "bad_config_no_mongodb_section.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: no mongodb section in config")


    def test_bad_config_no_index_keys(self):

        """ Given a config file with a mongodb section missing index keys, confirm failure. """

        config_filename = os.path.join(configs_dir, "bad_config_no_index_keys.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: no index_keys in mongodb section")


    def test_bad_config_no_secrets_section(self):

        """ Given a config file missing a secrets section, confirm failure. """

        config_filename = os.path.join(configs_dir, "bad_config_no_secrets_section.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: no secrets section")


    def test_bad_config_no_secrets_filename(self):

        """ Given a config file missing a secrets section, confirm failure. """

        config_filename = os.path.join(configs_dir, "bad_config_no_secrets_filename.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: no filename key in secrets section")


    def test_good_config_bad_secrets_no_mongodb_section(self):

        """ Given a secrets file with no mongodb section, confirm failure. """

        config_filename = os.path.join(configs_dir, "good_config_bad_secrets_no_mongodb_section.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: no mongodb section in secrets file")


    def test_good_config_bad_secrets_no_password(self):

        """ Given a secrets file with no password, confirm failure. """

        config_filename = os.path.join(configs_dir, "good_config_bad_secrets_no_password.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val.startswith("Error: no password in secrets file")


    def test_good_config_good_secrets(self):

        """ Given a good config file and a good secrets file, confirm success. """

        config_filename = os.path.join(configs_dir, "good_config_good_secrets.cfg")
        val= MetadataMongoIngester().open_connection(config_filename)
        assert val == None



    


