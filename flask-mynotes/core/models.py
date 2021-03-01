from peewee import *
from config import config
from datetime import datetime

db = SqliteDatabase(config.DB_NAME)


class User(Model):
    id = AutoField()
    name = CharField(max_length=128, index=True, unique=True)
    password_hash = CharField()
    created_at = DateField(default=datetime.now)

    class Meta:
        database = db
        table_name = "users"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "password_hash": self.password_hash, "created_at": self.created_at}


class Note(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='notes')
    title = CharField()
    text = TextField()
    created_at = DateField(default=datetime.now)

    class Meta:
        database = db
        table_name = "notes"

    def to_dict(self):
        return {"id": self.id, "user": self.user, "title": self.title,
                "text": self.text, "created_at": self.created_at}


def init_db():
    db.connect()
    db.create_tables([User, Note])
