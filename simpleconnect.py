#!/usr/bin/env python

import configparser
import sys
import os
import argparse
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import isi_sdk_8_0_1 as isi_sdk
from isi_sdk_8_0_1.rest import ApiException

class clusterConfig:

    def __init__(self, cluster):
        self.cluster = cluster
        self.open_config()
    
    def auth_settings(self):
        """
        Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        return {
            'basic_auth':
                {
                    'type': 'basic',
                    'in': 'header',
                    'key': 'Authorization',
                    'value': self.get_basic_auth_token()
                },

        }

    def get_basic_auth_token(self):
        """
        Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        #changed self.username to 
        return urllib3.util.make_headers(basic_auth=self.username + ':' + self.password)\
                           .get('authorization')    
    
    def open_config(self):
        config = configparser.ConfigParser()

        cf = os.path.join(
            #there is a note from here(https://qiita.com/zabeth129/items/dea3f71efd90546a2605) that asks for "__file__" in the interactive shell
            os.path.dirname(os.path.realpath("__file__")),
            "/Users/sbryant/bench/spiderdot/configs/isilon.cfg"
            )
        if not config.read([cf]):
            print("No configuration files found!")

        self.username = config.get(self.cluster, "username")
        self.password = config.get(self.cluster, "password")
        self.name = config.get(self.cluster, "hostname")
        self.host = config.get(self.cluster, "host")#"https://iodine.broadinstitute.org:8080"#"self.name"
        self.port = config.get(self.cluster, "port")
        self.verify_ssl = False #False works here but not when read from the config file # config.set(self.cluster, "verify_ssl")
        self.auth_settings = self.auth_settings
        self.get_basic_auth_token = self.get_basic_auth_token
        self.ssl_ca_cert = None #None works here but not when read from the config file # config.get(self.cluster, "ssl_ca_cert")
        self.assert_hostname = True
        self.connection_pool_maxsize = 10 #config.get(self.cluster, "connection_pool_maxsize") #10 # not sure what a good number what be 
        self.proxy = None #None works here but not when read from the config file # config.get(self.cluster, "proxy")
        self.api_version = config.get(self.cluster, "api_version")
        self.export_id = config.get(self.cluster, "export_id")
        self.cert_file = None #None works here but not in the config fileconfig.get(self.cluster, "cert_file")
        self.key_file = None #None works here but not in the config fileconfig.get(self.cluster, "key_file")
        self.safe_chars_for_path_param = config.get(self.cluster, "safe_chars_for_path_param")

def connect(cluster):
    config = configparser.ConfigParser()

    cf = os.path.join(
        os.path.dirname(os.path.realpath("__file__")),
        "/Users/sbryant/bench/spiderdot/configs/isilon.cfg"
    )
    if not config.read([cf]):
        print("No configuration files found!")
        return 1

    # Required configuration options
    configuration = isi_sdk.Configuration()
    configuration.username = config.get(cluster, "username")
    configuration.password = config.get(cluster, "password")
    host = config.get(cluster, "host")
    proxy = config.get(self.cluster, "proxy")

    # Optional configuration options
    try:
        configuration.verify_ssl = config.getboolean(
            cluster, "verify_ssl"
        )
    except configparser.NoOptionError:
        configuration.verify_ssl = False

    try:
        port = config.getint(cluster, "port")
    except configparser.NoOptionError:
        port = 8080

    uri = "https://%s:%d" % (host, port)
    configuration.host = uri
    api_client = isi_sdk.ApiClient(configuration)

    return api_client                
        


iod = clusterConfig('iodine')
# create an instance of the API class
api_instance = isi_sdk.NamespaceApi(isi_sdk.ApiClient(iod))
directory_metadata_path = '/ifs/stanley/genetics/analysis' # str | Directory path relative to /.
metadata = True # bool | Show directory metadata.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    api_response = api_instance.get_directory_metadata(directory_metadata_path, metadata)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NamespaceApi->get_directory_metadata: %s\n" % e)