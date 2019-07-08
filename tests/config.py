import os

from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure


if os.environ.get('GOOGLE_CLOUD_PROJECT') is None:
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'gumo-sample'

if os.environ.get('DATASTORE_EMULATOR_HOST') is None:
    os.environ['DATASTORE_EMULATOR_HOST'] = '127.0.0.1:8082'


core_configure()
datastore_configure()
