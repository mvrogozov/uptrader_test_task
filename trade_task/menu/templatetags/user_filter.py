from django import template
from django.shortcuts import get_object_or_404

from menu.models import Menu


register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu2(context, value):
    menu = get_object_or_404(Menu, menu__title=value)
    menu_data = menu.menu
    current_url = context['current_url']
    return {'items': [menu_data], 'current_url': current_url}


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, value):
    menu = get_object_or_404(Menu, menu__title=value)
    menu_data = menu.menu
    current_url = context['current_url']

    def make_menu(menu_data: dict, current_url, found_active: bool = False):
        res = list()
        if isinstance(menu_data, dict):
            data = menu_data.get('fields')
            if menu_data.get('url') == current_url:
                found_active = True
        else:
            data = menu_data
        for item in data:
            new_item = item.copy()
            new_item['fields'] = []
            if item.get('url') == current_url:
                found_active = True
                new_item['fields'], found_active = make_menu(
                    item.get('fields'),
                    current_url,
                    found_active
                )
            if found_active:
                res.append(new_item)
            else:
                new_item['fields'], found_active = make_menu(
                    item.get('fields'),
                    current_url,
                    found_active
                )
                res.append(new_item)
        if isinstance(menu_data, dict):
            menu_data['fields'] = res
            return menu_data
        return res, found_active

    return {
        'items': [make_menu(menu_data, current_url)],
        'current_url': current_url
    }
