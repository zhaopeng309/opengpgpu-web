from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.admin_service import AdminService
from app.services.announcement_service import AnnouncementService
from app.forms.admin_form import LoginForm

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = AdminService.verify_admin(username, password)
        
        if admin:
            login_user(admin)
            return redirect(url_for('admin_bp.dashboard'))
        flash('Invalid username or password')
        
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_bp.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    from app.services.roadmap_service import RoadmapService
    announcements = AnnouncementService.get_all()
    total_announcements = len(announcements)
    
    roadmaps_grouped = RoadmapService.get_all_roadmap_grouped()
    roadmap_stats = {}
    total_roadmaps = 0
    
    for stage, items in roadmaps_grouped.items():
        total_roadmaps += len(items)
        completed = sum(1 for item in items if item.status == 'completed')
        roadmap_stats[stage] = {
            'total': len(items),
            'completed': completed,
            'progress': int((completed / len(items)) * 100) if len(items) > 0 else 0
        }
        
    return render_template('admin/dashboard.html', 
                           total_announcements=total_announcements,
                           total_roadmaps=total_roadmaps,
                           roadmap_stats=roadmap_stats)

from app.forms.announcement_form import AnnouncementForm
from app.forms.admin_form import ChangePasswordForm

@admin_bp.route('/announcements')
@login_required
def announcements():
    items = AnnouncementService.get_all()
    return render_template('admin/announcements.html', announcements=items)

@admin_bp.route('/announcement/new', methods=['GET', 'POST'])
@login_required
def new_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        AnnouncementService.create_announcement(
            title=form.title.data,
            content=form.content.data,
            priority=form.priority.data or 0
        )
        flash('Announcement created successfully')
        return redirect(url_for('admin_bp.announcements'))
    return render_template('admin/announcement_form.html', form=form, title="New Announcement")

@admin_bp.route('/announcement/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    from app.dao.announcement_dao import AnnouncementDAO
    announcement = AnnouncementDAO.get_by_id(id)
    if not announcement:
        flash('Announcement not found')
        return redirect(url_for('admin_bp.announcements'))
        
    form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        AnnouncementService.update_announcement(
            id,
            title=form.title.data,
            content=form.content.data,
            priority=form.priority.data or 0,
            is_active=form.is_active.data
        )
        flash('Announcement updated successfully')
        return redirect(url_for('admin_bp.announcements'))
    return render_template('admin/announcement_form.html', form=form, title="Edit Announcement")

@admin_bp.route('/announcement/<int:id>/delete', methods=['POST'])
@login_required
def delete_announcement(id):
    AnnouncementService.delete_announcement(id)
    flash('Announcement deleted (soft delete) successfully')
    return redirect(url_for('admin_bp.announcements'))

from app.forms.roadmap_form import RoadmapForm
from app.services.roadmap_service import RoadmapService

@admin_bp.route('/roadmaps')
@login_required
def roadmaps():
    grouped_items = RoadmapService.get_all_roadmap_grouped()
    return render_template('admin/roadmaps.html', grouped_roadmaps=grouped_items)

@admin_bp.route('/roadmap/new', methods=['GET', 'POST'])
@login_required
def new_roadmap():
    form = RoadmapForm()
    if form.validate_on_submit():
        RoadmapService.create_roadmap_item(
            title=form.title.data,
            stage=form.stage.data,
            status=form.status.data,
            description=form.description.data,
            order=form.order.data or 0
        )
        flash('Roadmap item created successfully')
        return redirect(url_for('admin_bp.roadmaps'))
    return render_template('admin/roadmap_form.html', form=form, title="New Roadmap Item")

@admin_bp.route('/roadmap/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_roadmap(id):
    from app.dao.roadmap_dao import RoadmapDAO
    roadmap = RoadmapDAO.get_by_id(id)
    if not roadmap:
        flash('Roadmap item not found')
        return redirect(url_for('admin_bp.roadmaps'))
        
    form = RoadmapForm(obj=roadmap)
    if form.validate_on_submit():
        RoadmapService.update_roadmap_item(
            id,
            title=form.title.data,
            stage=form.stage.data,
            status=form.status.data,
            description=form.description.data,
            order=form.order.data or 0
        )
        flash('Roadmap item updated successfully')
        return redirect(url_for('admin_bp.roadmaps'))
    return render_template('admin/roadmap_form.html', form=form, title="Edit Roadmap Item")

@admin_bp.route('/roadmap/<int:id>/delete', methods=['POST'])
@login_required
def delete_roadmap(id):
    RoadmapService.delete_roadmap_item(id)
    flash('Roadmap item deleted successfully')
    return redirect(url_for('admin_bp.roadmaps'))

@admin_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            AdminService.change_password(
                admin_id=current_user.id,
                current_password=form.current_password.data,
                new_password=form.new_password.data
            )
            flash('Password changed successfully')
            return redirect(url_for('admin_bp.dashboard'))
        except ValueError as e:
            flash(str(e))
    
    return render_template('admin/change_password.html', form=form)
