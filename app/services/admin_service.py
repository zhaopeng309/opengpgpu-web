from app.dao.admin_dao import AdminDAO
from app.models.admin import Admin

class AdminService:
    @staticmethod
    def register_admin(username, password):
        if AdminDAO.get_by_username(username):
            raise ValueError("Admin already exists")
        
        admin = Admin()
        admin.username = username
        admin.set_password(password)
        admin.save()
        return admin

    @staticmethod
    def verify_admin(username, password):
        admin = AdminDAO.get_by_username(username)
        if admin and admin.check_password(password):
            return admin
        return None

    @staticmethod
    def change_password(admin_id, current_password, new_password):
        admin = AdminDAO.get_by_id(admin_id)
        if not admin:
            raise ValueError("Admin not found")
        
        if not admin.check_password(current_password):
            raise ValueError("Current password is incorrect")
        
        admin.set_password(new_password)
        admin.save()
        return admin
