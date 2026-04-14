import pytest
from app.services.admin_service import AdminService
from app.services.announcement_service import AnnouncementService
from app.services.roadmap_service import RoadmapService

def test_admin_service(app):
    AdminService.register_admin('admin', 'password')
    with pytest.raises(ValueError, match="Admin already exists"):
        AdminService.register_admin('admin', 'newpassword')
    
    assert AdminService.verify_admin('admin', 'password') is not None
    assert AdminService.verify_admin('admin', 'wrongpass') is None

def test_announcement_service(app):
    with pytest.raises(ValueError, match="Title too long"):
        AnnouncementService.create_announcement('a' * 101, 'content')
        
    ann = AnnouncementService.create_announcement('Title', 'Content')
    assert len(AnnouncementService.get_latest_announcements()) == 1
    
    AnnouncementService.delete_announcement(ann.id)
    assert len(AnnouncementService.get_latest_announcements()) == 0

def test_roadmap_service(app):
    with pytest.raises(ValueError, match="Invalid status"):
        RoadmapService.create_roadmap_item('Title', 'Q1 2024', status='invalid')
        
    RoadmapService.create_roadmap_item('Item 1', 'Q1 2024')
    RoadmapService.create_roadmap_item('Item 2', 'Q1 2024')
    grouped = RoadmapService.get_all_roadmap_grouped()
    assert len(grouped['Q1 2024']) == 2
