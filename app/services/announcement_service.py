from app.dao.announcement_dao import AnnouncementDAO

class AnnouncementService:
    @staticmethod
    def create_announcement(title, content, priority=0):
        if len(title) > 100:
            raise ValueError("Title too long")
        return AnnouncementDAO.create(title=title, content=content, priority=priority)

    @staticmethod
    def get_latest_announcements(limit=5):
        return AnnouncementDAO.get_active_announcements(limit=limit)

    @staticmethod
    def get_all():
        return AnnouncementDAO.get_all()

    @staticmethod
    def update_announcement(id, **kwargs):
        if 'title' in kwargs and len(kwargs['title']) > 100:
            raise ValueError("Title too long")
        return AnnouncementDAO.update(id, **kwargs)

    @staticmethod
    def delete_announcement(id):
        return AnnouncementDAO.update(id, is_active=False)
