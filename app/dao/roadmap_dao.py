from app.dao.base_dao import BaseDAO
from app.models.roadmap import Roadmap
from app.extensions import db

class RoadmapDAO(BaseDAO):
    model = Roadmap

    @classmethod
    def get_all_ordered(cls):
        return db.session.query(cls.model).order_by(cls.model.stage, cls.model.order).all()
        
    @classmethod
    def get_by_stage(cls, stage):
        return db.session.query(cls.model).filter_by(stage=stage).order_by(cls.model.order).all()
