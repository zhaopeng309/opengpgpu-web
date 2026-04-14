from app.extensions import db

class BaseDAO:
    model = None

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls.model, id)

    @classmethod
    def get_all(cls):
        return db.session.query(cls.model).all()

    @classmethod
    def filter_by(cls, **kwargs):
        return db.session.query(cls.model).filter_by(**kwargs).all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls.model(**kwargs)
        instance.save()
        return instance

    @classmethod
    def update(cls, id, **kwargs):
        instance = cls.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
        return instance

    @classmethod
    def delete(cls, id):
        instance = cls.get_by_id(id)
        if instance:
            instance.delete()
            return True
        return False
        
    @classmethod
    def count(cls):
        return db.session.query(cls.model).count()
