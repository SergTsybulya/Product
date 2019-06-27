
from django.conf.urls import url

from product.views import ProductListView

urlpatterns = [
        url(r'^(?P<product>[a-zA-Z]+)/$', ProductListView.as_view(), name="product"),
                ]
