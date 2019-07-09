import flask
import logging
import sys
import os
import datetime

from gumo.core import configure as core_configure
from gumo.datastore.infrastructure import DatastoreRepositoryMixin
from gumo.datastore.infrastructure import DatastoreEntity


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SampleRepository(DatastoreRepositoryMixin):
    KIND = 'SampleEntity'

    def save(self, name: str):
        entity = DatastoreEntity(key=self.datastore_client.key(self.KIND, name))
        entity['name'] = name
        entity['updated_at'] = datetime.datetime.utcnow()
        self.datastore_client.put(entity)

    def fetch_entities(self):
        query = self.datastore_client.query(kind=self.KIND)
        query.order = ['-updated_at']
        return list(query.fetch())

    def fetch_count(self):
        query = self.datastore_client.query(kind=self.KIND)
        query.keys_only()
        return len(list(query.fetch()))


if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'gumo-datastore-test'

core_configure()


app = flask.Flask(__name__)


@app.route('/')
def hello():
    return f'Hello, world. (gumo-datastore)'


@app.route('/fetch')
def fetch():
    entities = SampleRepository().fetch_entities()

    return flask.Response(
        '\n'.join([str(e) for e in entities]),
        content_type='text/plain'
    )


@app.route('/create')
def create():
    name = flask.request.args.get('name')
    if name is None:
        return f'Please set name arguments.'

    SampleRepository().save(name=name)
    return 'created. Please check /fetch'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
