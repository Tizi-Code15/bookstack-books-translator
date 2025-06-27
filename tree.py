import os

def print_tree(startpath, exclude_dirs=None, prefix=""):
    if exclude_dirs is None:
        exclude_dirs = []

    items = sorted(os.listdir(startpath))
    items = [item for item in items if item not in exclude_dirs]

    for index, item in enumerate(items):
        path = os.path.join(startpath, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            print_tree(path, exclude_dirs, prefix + extension)

if __name__ == "__main__":
    dossier_a_explorer = "." 
    dossiers_a_exclure = ["env", "__pycache__", ".git"] 

    print_tree(dossier_a_explorer, exclude_dirs=dossiers_a_exclure)