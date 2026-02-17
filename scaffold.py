import os
import re
import shutil

PROJECT_ROOT = r"c:\Users\stanl\Desktop\vscodeprojects\citizen-zero"
STRUCTURE_DIR = os.path.join(PROJECT_ROOT, "project-structure")

STRUCTURE_FILES = {
    "flutter": "flutter-mobile-structure.txt",
    "backend": "django-backend-services-structure.txt",
    "web": "web-application-structure.txt",
    "cli": "cli-application-structure.txt",
    "desktop": "desktop-application-structure.txt",
    "docs": "documentation-structure.txt",
    "scripts": "scripts-structure.txt",
    "tests": "tests-structure.txt",
    "data": "data-structure.txt"
}

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.parent = parent
        self.is_explicit_dir = name.endswith('/')
        
    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def is_directory(self):
        # A node is a directory if it has children OR it ends with / OR it doesn't have an extension (mostly)
        if self.children:
            return True
        if self.is_explicit_dir:
            return True
        # Heuristic for leaf nodes:
        if '.' in self.name and not self.name.startswith('.'): # Extension present -> File
            return False
        if self.name in ['Makefile', 'Dockerfile', 'LICENSE']:
            return False
        # Default to directory if no extension (unless excluded)
        return True

def clean_line(line):
    # Remove comments
    line = line.split('#')[0].rstrip()
    if not line:
        return None, 0
    
    # regex to find the start of the name
    match = re.search(r'[a-zA-Z0-9_\.]', line)
    if not match:
        return None, 0
    
    start_index = match.start()
    name = line[start_index:].strip()
    prefix = line[:start_index]
    
    # calculate depth based on 4-char blocks roughly
    depth = len(prefix) // 4
    return name, depth

def build_tree(lines):
    root = Node("root")
    # Stack: [(depth, node)]
    stack = [(-1, root)]
    
    for line in lines:
        line = line.rstrip()
        if not line or line.startswith("Summary:"):
            continue
            
        name, depth = clean_line(line)
        if not name:
            continue
            
        node = Node(name)
        
        # Find parent
        while stack and stack[-1][0] >= depth:
            stack.pop()
            
        parent = stack[-1][1]
        parent.add_child(node)
        
        stack.append((depth, node))
        
    return root

def create_fs(node, current_path):
    # Don't create root node itself as a folder literal "root"
    if node.name == "root":
        for child in node.children:
            create_fs(child, current_path)
        return

    clean_name = node.name.rstrip('/')
    # If the text file starts with the root folder name (e.g. flutter/), avoid duplicating if current_path already ends with it
    # But usually parsing attaches it as a child of root.
    # Logic: if node is "flutter/" and current_path is PROJECT_ROOT, path is PROJECT_ROOT/flutter
    
    my_path = os.path.join(current_path, clean_name)
    
    if node.is_directory():
        # Check if it exists as a file and remove it if so (fix previous error)
        if os.path.isfile(my_path):
            print(f"[FIX] Removing file {my_path} to replace with directory")
            os.remove(my_path)
            
        if not os.path.exists(my_path):
            try:
                os.makedirs(my_path)
                print(f"[DIR] {my_path}")
            except Exception as e:
                print(f"Error creating dir {my_path}: {e}")
        
        for child in node.children:
            create_fs(child, my_path)
    else:
        # File
        if node.children:
            # Should have been a directory caught above?
            # Re-check logic: is_directory() returns True if children exist.
            pass
            
        if not os.path.exists(my_path) and not os.path.isdir(my_path):
            try:
                parent = os.path.dirname(my_path)
                if not os.path.exists(parent):
                    os.makedirs(parent)
                with open(my_path, 'w') as f:
                    pass
                print(f"[FILE] {my_path}")
            except Exception as e:
                print(f"Error creating file {my_path}: {e}")

def main():
    for key, filename in STRUCTURE_FILES.items():
        full_path = os.path.join(STRUCTURE_DIR, filename)
        print(f"Processing {full_path}...")
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            root = build_tree(lines)
            
            # If the structure file describes "flutter/..." then root's child is "flutter"
            # We want to create that under PROJECT_ROOT.
            
            create_fs(root, PROJECT_ROOT)
            
        except FileNotFoundError:
            print(f"Error: File not found: {full_path}")

    # Ensure .github/workflows
    github_dir = os.path.join(PROJECT_ROOT, ".github", "workflows")
    os.makedirs(github_dir, exist_ok=True)
    
    # Root config files
    root_files = [".env.example", "docker-compose.yml", "Makefile", "README.md", "LICENSE"]
    for rf in root_files:
        p = os.path.join(PROJECT_ROOT, rf)
        if not os.path.exists(p):
            with open(p, 'w') as f:
                f.write(f"# Placeholder for {rf}")
            print(f"[ROOT] Created {p}")

if __name__ == "__main__":
    main()
