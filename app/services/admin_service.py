from app.dao.admin_dao import AdminDAO
from app.models.admin import Admin

class AdminService:
    @staticmethod
    def register_admin(username, password):
        if AdminDAO.get_by_username(username):
            raise ValueError("Admin already exists")
        
        admin = Admin(username=username)
        admin.set_password(password)
        admin.save()
        return admin

    @staticmethod
    def verify_admin(username, password):
        admin = AdminDAO.get_by_username(username)
        if admin and admin.check_password(password):
            return admin
        return None
