# Model module
from provider.database import db
import peewee_async


class BaseModel(peewee_async.AioModel):

    class Meta:
        database = db
