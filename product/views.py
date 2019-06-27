
from django.conf import settings
from django.core.mail import send_mail

from django.views.generic import ListView, DetailView, FormView

from core.forms import RequestForm
from product.models import Product


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.active_product()

    def get_queryset(self):
        qs = super().get_queryset()
        product = self.kwargs.get('product')
        if product:
            query = qs.filter(category__slug=product)
            return query
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('product')
        return context

    def get_success_url(self):
        return self.request.build_absolute_uri
