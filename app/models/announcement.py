from app.extensions import db
from app.models.base import BaseModel

class Announcement(BaseModel):
    __tablename__ = 'announcements'

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, default=0) # 0: Normal, 1: High
    is_active = db.Column(db.Boolean, default=True)
