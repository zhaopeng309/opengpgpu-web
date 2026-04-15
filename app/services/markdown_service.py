import os
import markdown
import re

class MarkdownService:
    @staticmethod
    def get_title_from_md(filepath):
        """Extract the first H1 header or use the filename without extension."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('# '):
                        return line[2:].strip()
        except Exception:
            pass
        
        # Fallback to filename
        return os.path.splitext(os.path.basename(filepath))[0].replace('_', ' ')

    @staticmethod
    def build_file_tree(base_path, current_path=""):
        """
        Recursively scan the directory and build a tree structure.
        Only includes directories and .md files.
        """
        tree = []
        full_path = os.path.join(base_path, current_path)
        
        if not os.path.exists(full_path):
            return tree

        # Sort entries: directories first, then files
        entries = sorted(os.listdir(full_path))
        dirs = []
        files = []
        
        for entry in entries:
            # Ignore hidden files/folders
            if entry.startswith('.'):
                continue
                
            entry_full_path = os.path.join(full_path, entry)
            entry_rel_path = os.path.join(current_path, entry).replace('\\', '/')
            
            if os.path.isdir(entry_full_path):
                sub_tree = MarkdownService.build_file_tree(base_path, entry_rel_path)
                if sub_tree: # Only add if the directory is not empty (contains md files)
                    dirs.append({
                        'type': 'dir',
                        'name': entry.replace('_', ' '),
                        'children': sub_tree
                    })
            elif os.path.isfile(entry_full_path) and entry.endswith('.md'):
                # Handle path routing: remove .md for the route path
                route_path = entry_rel_path[:-3]
                files.append({
                    'type': 'file',
                    'name': MarkdownService.get_title_from_md(entry_full_path),
                    'path': route_path,
                    'filename': entry
                })
                
        tree.extend(dirs)
        tree.extend(files)
        return tree

    @staticmethod
    def parse_markdown(content):
        """
        Parse markdown content to HTML.
        Returns a tuple: (html_content, toc_html)
        """
        # Pre-process mermaid code blocks to raw HTML so markdown doesn't parse them as code blocks
        content = re.sub(
            r'```mermaid\s*\n(.*?)\n```',
            r'<div class="mermaid">\n\1\n</div>',
            content,
            flags=re.DOTALL
        )

        md = markdown.Markdown(extensions=[
            'markdown.extensions.toc',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.codehilite'
        ])
        
        html_content = md.convert(content)
        toc_html = md.toc
        
        return html_content, toc_html
