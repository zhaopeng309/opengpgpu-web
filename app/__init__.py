from flask import Flask
from config import config
from app.extensions import db, bcrypt, login_manager

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.dao.admin_dao import AdminDAO
        return AdminDAO.get_by_id(int(user_id))

    from app.views.frontend import frontend_bp
    from app.views.admin import admin_bp
    app.register_blueprint(frontend_bp)
    app.register_blueprint(admin_bp)

    return app
