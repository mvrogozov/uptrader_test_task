from django import template
from django.shortcuts import get_object_or_404
from django.urls import reverse, NoReverseMatch

from menu.models import Menu


register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, value):
    menu = get_object_or_404(Menu, menu__title=value)
    menu_data = menu.menu
    current_url = context['current_url']

    def resolve_url(url):
        try:
            if ':' in url:
                url = url.split()
                if len(url) > 1:
                    nurl, params = url
                    return reverse(nurl, args=[params])
                return reverse(url[0])
            return reverse('menu:dynamic_page', kwargs={'page_name': url})
        except NoReverseMatch:
            return url

    def make_menu(menu_data: dict, current_url, found_active: bool = False):
        res = list()
        if isinstance(menu_data, dict):
            data = menu_data.get('fields')
            url = resolve_url(menu_data.get('url'))
            menu_data['url'] = url
            if url == resolve_url(current_url):
                found_active = True
        else:
            data = menu_data
        for item in data:
            new_item = item.copy()
            new_item['fields'] = []
            url = resolve_url(item.get('url'))
            new_item['url'] = url
            if url == resolve_url(current_url):
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
