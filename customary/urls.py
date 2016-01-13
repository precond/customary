from django.conf.urls import url

from customary.api import views


urlpatterns = [
    url('status/$', views.status, name='customary_status')
]
