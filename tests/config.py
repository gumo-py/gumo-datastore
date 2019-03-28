from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure


core_configure(
    google_cloud_project='gumo-sample',
    google_cloud_location='asia-northeast1',
)

datastore_configure(
    use_local_emulator=True,
    emulator_host='datastore_emulator:8081',
    namespace=None,
)
