from flask import Blueprint, render_template
from app.services.announcement_service import AnnouncementService
from app.services.roadmap_service import RoadmapService

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    announcements = AnnouncementService.get_latest_announcements(limit=5)
    return render_template('index.html', announcements=announcements)

@frontend_bp.route('/roadmap')
def roadmap():
    roadmap_data = RoadmapService.get_all_roadmap_grouped()
    return render_template('roadmap.html', roadmap_data=roadmap_data)

@frontend_bp.route('/docs')
def docs():
    return render_template('docs.html')

@frontend_bp.route('/community')
def community():
    return render_template('community.html')
