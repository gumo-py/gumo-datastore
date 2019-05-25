import os

from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '.circleci',
        'gumo-example-173c5119a29a.json'
    )

if os.environ.get('DATASTORE_EMULATOR_HOST') is None:
    os.environ['DATASTORE_EMULATOR_HOST'] = '127.0.0.1:8082'


core_configure(
    google_cloud_project='gumo-sample',
    google_cloud_location='asia-northeast1',
)

datastore_configure(
    use_local_emulator=True,
    emulator_host=os.environ.get('DATASTORE_EMULATOR_HOST'),
    namespace=None,
)
