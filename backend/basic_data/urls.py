from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /basic_data/request/
    url(r'^request/$', views.service_request, name='request'),
]