from django.conf import settings
from datetime import timedelta

AG_GRID_JS = getattr(settings, 'DJ_AG_GRID_JS',
                     'https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js')
AG_GRID_CSS = getattr(settings, 'DJ_AG_GRID_CSS', 'https://unpkg.com/ag-grid/dist/styles/ag-grid.css')
AG_GRID_THEME = getattr(settings, 'DJ_AG_GRID_THEME', 'https://unpkg.com/ag-grid/dist/styles/ag-theme-balham.css')
AG_GRID_LOCALE = getattr(settings, 'DJ_AG_GRID_LOCALE', 'en-US')
AG_GRID_LOCALE_CACHE = getattr(settings, 'DJ_AG_GRID_LOCALE_CACHE', timedelta(days=7).total_seconds())
