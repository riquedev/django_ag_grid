import json
import re
from django import template
from django.core.cache import cache
from django.urls import resolve, reverse
from django_ag_grid.settings import AG_GRID_JS, AG_GRID_CSS, AG_GRID_THEME, AG_GRID_LOCALE, AG_GRID_LOCALE_CACHE
from requests import Session

register = template.Library()


@register.inclusion_tag('ag_grid/dependencies.html', takes_context=True)
def render_ag_grid_dependencies(context):
    context['js'] = AG_GRID_JS
    context['css'] = AG_GRID_CSS
    context['theme'] = AG_GRID_THEME
    return context


@register.inclusion_tag('ag_grid/grid.html', takes_context=True)
def render_ag_grid(context, url_name,
                   grid_id: str = None,
                   grid_class: str = None,
                   default_col_def: str = '',
                   style: str = 'height: 100%; width: 100%',
                   **kwargs
                   ):
    url_path = reverse(url_name)
    view_func = resolve(url_path).func

    if 'rowModelType' not in kwargs:
        kwargs['rowModelType'] = 'infinite'

    try:
        default_col_def = json.loads(default_col_def) if default_col_def else {}
    except json.decoder.JSONDecodeError:
        default_col_def = {}

    assert hasattr(view_func, 'view_class'), 'Only class based views supported'
    view_class = view_func.view_class
    context['grid_id'] = grid_id if grid_id else 'data-grid'
    context['grid_class'] = grid_class if grid_class else 'ag-theme-balham'
    context['column_defs'] = view_class.column_defs
    context['url_path'] = url_path
    context['default_col_def'] = json.dumps(default_col_def)
    context['style'] = style
    cache_key = f'AG_GRID_LOCALE_{AG_GRID_LOCALE}'
    locale_text = cache.get(cache_key)

    if not locale_text:
        with Session() as handler:
            url = f'https://raw.githubusercontent.com/ag-grid/ag-grid/latest/community-modules/locale/src/{AG_GRID_LOCALE}.ts'

            with handler.get(url) as response:
                locale_text = re.search(r'export\s+const\s+\w+\s*=\s*({.*?});',
                                        response.content.decode('utf-8'), re.DOTALL).group(1)
                cache.set(cache_key, locale_text, int(AG_GRID_LOCALE_CACHE))

    context['locale_text'] = locale_text
    context['additional_settings'] = json.dumps(kwargs)
    return context
