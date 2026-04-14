from app.dao.base_dao import BaseDAO
from app.models.admin import Admin
from app.extensions import db

class AdminDAO(BaseDAO):
    model = Admin

    @classmethod
    def get_by_username(cls, username):
        return db.session.query(cls.model).filter_by(username=username).first()
