from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import IndexView, DynamicPageView

app_name = 'menu'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(
        'pages/<str:page_name>',
        DynamicPageView.as_view(),
        name='dynamic_page'
    ),
]
