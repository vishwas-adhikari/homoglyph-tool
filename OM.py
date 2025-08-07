import os

project_structure = [
    ".gitignore",
    "manage.py",
    "package.json",
    "homoglyph_project/__init__.py",
    "homoglyph_project/settings.py",
    "homoglyph_project/urls.py",
    "homoglyph_app/__init__.py",
    "homoglyph_app/apps.py",
    "homoglyph_app/urls.py",
    "homoglyph_app/views.py",
    "homoglyph_app/data/chars.txt",
    "homoglyph_app/core/homoglyph_data.py",
    "homoglyph_app/utils/detector.py",
    "homoglyph_app/utils/generator.py",
    "homoglyph_app/static/homoglyph_app/css/style.css",
    "homoglyph_app/static/homoglyph_app/js/main.js",
    "homoglyph_app/templates/homoglyph_app/index.html",
]

for path in project_structure:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    if not path.endswith("/"):
        open(path, 'a').close()

print("Project structure created!")
