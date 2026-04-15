from flask import Blueprint, render_template, current_app, abort
from app.services.announcement_service import AnnouncementService
from app.services.roadmap_service import RoadmapService
from app.services.markdown_service import MarkdownService
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    announcements = AnnouncementService.get_latest_announcements(limit=5)
    return render_template('index.html', announcements=announcements)

@frontend_bp.route('/roadmap')
def roadmap():
    roadmap_data = RoadmapService.get_all_roadmap_grouped()
    return render_template('roadmap.html', roadmap_data=roadmap_data)

@frontend_bp.route('/docs', defaults={'filepath': 'index'})
@frontend_bp.route('/docs/<path:filepath>')
def docs(filepath):
    # docs directory at project root or configured
    base_docs_path = current_app.config.get('DOCS_DIR')
    if not base_docs_path:
        base_docs_path = os.path.join(current_app.root_path, '..', 'docs')
        base_docs_path = os.path.abspath(base_docs_path)

    # Build the file tree
    file_tree = MarkdownService.build_file_tree(base_docs_path)
    
    # Check if a specific file was requested. If 'index' is requested but doesn't exist, 
    # try to serve the first available document.
    target_file = os.path.join(base_docs_path, f"{filepath}.md")
    
    # If filepath is a directory, it might try to read an index.md inside it
    if os.path.isdir(os.path.join(base_docs_path, filepath)):
        target_file = os.path.join(base_docs_path, filepath, "index.md")
        
    if not os.path.exists(target_file) and filepath == 'index':
        # Find first file in tree
        def find_first_file(tree):
            for item in tree:
                if item['type'] == 'file':
                    return item
                elif item['type'] == 'dir' and item['children']:
                    res = find_first_file(item['children'])
                    if res: return res
            return None
        
        first_file = find_first_file(file_tree)
        if first_file:
            target_file = os.path.join(base_docs_path, f"{first_file['path']}.md")
            # Update current_path for active link
            filepath = first_file['path']
    
    if not os.path.exists(target_file):
        abort(404)
        
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        html_content, toc_html = MarkdownService.parse_markdown(content)
        
        return render_template('docs.html', 
                               html_content=html_content, 
                               toc_html=toc_html, 
                               file_tree=file_tree,
                               current_path=filepath)
    except Exception as e:
        abort(500)

@frontend_bp.route('/community')
def community():
    return render_template('community.html')
