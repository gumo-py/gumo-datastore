import dataclasses
import datetime
from typing import ClassVar
from typing import List
from typing import Tuple
from typing import Union
from typing import Optional

from gumo.datastore.infrastructure.alias import DatastoreEntity
from gumo.datastore.infrastructure.alias import DatastoreKey


@dataclasses.dataclass()
class DataModel:
    key: DatastoreKey

    exclude_from_indexes: ClassVar[Union[List[str], Tuple[str, ...]]] = []
    DatastoreEntity: ClassVar = DatastoreEntity
    DatastoreKey: ClassVar = DatastoreKey

    def to_datastore_entity(self) -> DatastoreEntity:
        raise NotImplementedError()

    @classmethod
    def from_datastore_entity(cls, doc: DatastoreEntity) -> "DataModel":
        raise NotImplementedError()

    @classmethod
    def convert_optional_datetime(
        cls, t: Optional[datetime.datetime]
    ) -> Optional[datetime.datetime]:
        if t is None:
            return None

        return cls.convert_datetime(t)

    @classmethod
    def convert_datetime(cls, t: datetime.datetime) -> datetime.datetime:
        return datetime.datetime(
            year=t.year,
            month=t.month,
            day=t.day,
            hour=t.hour,
            minute=t.minute,
            second=t.second,
            microsecond=t.microsecond,
            tzinfo=datetime.timezone.utc,
        )
