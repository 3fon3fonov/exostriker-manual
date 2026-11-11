"""Documentation-only configuration: do not import Qt or numerical extensions."""
project = 'Exo-Striker'
author = 'Exo-Striker contributors'
copyright = '2026, Exo-Striker contributors'
version = '0.97.1'
release = '0.97.1 (development checkout)'
extensions = []
master_doc = 'index'
source_suffix = '.rst'
exclude_patterns = ['_build', 'conf.py.save']
html_theme = 'sphinx_rtd_theme'
html_title = 'Exo-Striker user and API manual'
html_theme_options = {'navigation_depth': 4, 'collapse_navigation': True}
html_static_path = ['_static']
html_css_files = ['manual.css']
html_last_updated_fmt = '%Y-%m-%d'
