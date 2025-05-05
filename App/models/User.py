from app.config.db import db
from orator import Model, SoftDeletes
import pendulum

Model.set_connection_resolver(db)

class User(SoftDeletes,Model):
    __table__   = 'users' 
    __guarded__ = ['id']
    __dates__   = ['deleted_at']

    def fresh_timestamp(self):
        return pendulum.now("Asia/Jakarta")

    def get_by_username(username):
        data = User.where('username', username).first()
        if data is not None:
            data = data.serialize()
        return data

    def get_by_roles(roles):
        data = User.where('roles', roles).first()
        if data is not None:
            data = data.serialize()
        return data