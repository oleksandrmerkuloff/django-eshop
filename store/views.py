from django.http import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView



from typing import Any

from store.models import Product, Category


class StorePageView(TemplateView):
    template_name = 'store/home-page.html'
    model = Product
    context_object_name = 'products'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        pass
