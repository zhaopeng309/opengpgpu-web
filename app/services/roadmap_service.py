from app.dao.roadmap_dao import RoadmapDAO

class RoadmapService:
    VALID_STATUSES = ['pending', 'in_progress', 'completed']

    @staticmethod
    def create_roadmap_item(title, stage, status='pending', description=None, order=0):
        if status not in RoadmapService.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of {RoadmapService.VALID_STATUSES}")
        if not title:
            raise ValueError("Title cannot be empty")
        
        return RoadmapDAO.create(title=title, stage=stage, status=status, description=description, order=order)

    @staticmethod
    def get_all_roadmap_grouped():
        items = RoadmapDAO.get_all_ordered()
        grouped = {}
        for item in items:
            if item.stage not in grouped:
                grouped[item.stage] = []
            grouped[item.stage].append(item)
        return grouped

    @staticmethod
    def update_roadmap_item(id, **kwargs):
        if 'status' in kwargs and kwargs['status'] not in RoadmapService.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of {RoadmapService.VALID_STATUSES}")
        return RoadmapDAO.update(id, **kwargs)

    @staticmethod
    def delete_roadmap_item(id):
        return RoadmapDAO.delete(id)
