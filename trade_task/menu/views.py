from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'menu/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_url'] = self.kwargs.get(
            'page_name',
            'menu/index.html'
        )
        return context


class DynamicPageView(TemplateView):
    def get_template_names(self) -> list[str]:
        page_name = self.kwargs.get('page_name', 'menu/index.html')
        return [f'pages/{page_name}.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_url'] = self.request.path
        return context
