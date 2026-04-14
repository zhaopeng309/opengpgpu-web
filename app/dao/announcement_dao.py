from app.dao.base_dao import BaseDAO
from app.models.announcement import Announcement
from app.extensions import db

class AnnouncementDAO(BaseDAO):
    model = Announcement

    @classmethod
    def get_active_announcements(cls, limit=None):
        query = db.session.query(cls.model).filter_by(is_active=True).order_by(cls.model.priority.desc(), cls.model.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
