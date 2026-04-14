import os
from app import create_app
from app.extensions import db
from app.services.admin_service import AdminService
from app.services.announcement_service import AnnouncementService
from app.services.roadmap_service import RoadmapService

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
    from app.models.admin import Admin
    from app.models.announcement import Announcement
    from app.models.roadmap import Roadmap
    
    db.create_all()
    
    # Create admin
    try:
        AdminService.register_admin('admin', 'admin123')
        print("Admin user created.")
    except ValueError:
        print("Admin user already exists.")
        
    # Create some announcements
    try:
        AnnouncementService.create_announcement('OpenGPGPU Launched', 'Welcome to the official OpenGPGPU project website!', 1)
        AnnouncementService.create_announcement('v0.1 Beta Released', 'We are happy to announce the beta release.', 0)
        print("Announcements created.")
    except Exception as e:
        print(f"Announcement error: {e}")
        
    # Create roadmap items
    try:
        RoadmapService.create_roadmap_item('Initial Architecture Design', 'Q1 2024', 'completed', 'Design the core architecture.')
        RoadmapService.create_roadmap_item('Beta Release', 'Q2 2024', 'in_progress', 'Release the first beta version.')
        RoadmapService.create_roadmap_item('1.0 Release', 'Q3 2024', 'pending', 'Official 1.0 release.')
        print("Roadmap items created.")
    except Exception as e:
        print(f"Roadmap error: {e}")
        
    print("Database initialization complete.")
