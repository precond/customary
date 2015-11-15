from django.conf.urls import url


urlpatterns = [
    url('status/$', 'customary.api.views.status', name='customary_status')
]
