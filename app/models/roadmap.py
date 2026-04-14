from app.extensions import db
from app.models.base import BaseModel

class Roadmap(BaseModel):
    __tablename__ = 'roadmaps'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    stage = db.Column(db.String(50), nullable=False) # e.g., 'Q1 2024', 'Q2 2024'
    status = db.Column(db.String(20), default='pending') # pending, in_progress, completed
    order = db.Column(db.Integer, default=0)
