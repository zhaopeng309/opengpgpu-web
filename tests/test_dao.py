from app.dao.admin_dao import AdminDAO
from app.dao.announcement_dao import AnnouncementDAO
from app.dao.roadmap_dao import RoadmapDAO

def test_admin_dao(app):
    admin = AdminDAO.create(username='admin', password_hash='hash')
    assert admin.id is not None
    
    fetched = AdminDAO.get_by_username('admin')
    assert fetched.id == admin.id

def test_announcement_dao(app):
    AnnouncementDAO.create(title='A1', content='C1', priority=1)
    AnnouncementDAO.create(title='A2', content='C2', priority=0)
    AnnouncementDAO.create(title='A3', content='C3', is_active=False)
    
    active = AnnouncementDAO.get_active_announcements()
    assert len(active) == 2
    assert active[0].title == 'A1'

def test_roadmap_dao(app):
    RoadmapDAO.create(title='R1', stage='Q1', order=2)
    RoadmapDAO.create(title='R2', stage='Q1', order=1)
    RoadmapDAO.create(title='R3', stage='Q2', order=1)
    
    q1_items = RoadmapDAO.get_by_stage('Q1')
    assert len(q1_items) == 2
    assert q1_items[0].title == 'R2'
