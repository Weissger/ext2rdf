__author__ = 'tmy'

import os
import sys
import configparser
import logging

# Utilities.Logger not importable due to need of Utilities.Constants
log = logging.getLogger("OpenIE2RDF")

# find preferences file
current_path = os.getcwd()
parent_paths = [os.getcwd()]

for i in range(0, 6):
    parent_paths.append('{}{}..'.format(parent_paths[i], os.sep))

possible_paths = []
for path in parent_paths:
    possible_paths.append('{}{}data'.format(path, os.sep))

config_paths = [i + os.sep + 'preferences.ini' for i in possible_paths]

config_file = [path for path in config_paths if os.path.isfile(path)][0]

# read config file and set constants
config = configparser.ConfigParser()
config.read(config_file, encoding='utf-8')

if not config.has_section('app'):
    log.error("Preferences.ini not found or malformed")
    sys.exit()

# additional dynamic options
config.set('app', 'data_path', config_file[:-15])

programs = {
    'oIE': "openIE",
    'rvb': "reverb"
}

arg_types = {
    'rel': "relation",
    'simple': "simple",
    'tmp': "temporal",
    'spatial': "spatial"
}

SEPARATOR = '\t'
SUB_SEPARATOR = ' | '

E2RDF_COLUMN_NAMES = ["Confidence", "Context", "Subject", "Predicate", "Object", "Other_arg", "Temporal", "Spatial",
                      "Sentence_id", "Sentence"]

del config_file
del config_paths
del current_path
del possible_paths
