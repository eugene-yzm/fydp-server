from django.conf.urls import url, include
from rest_framework import routers
from api import views
from django.contrib import admin

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^data/$', views.data_list),
    url(r'^data/(?P<pk>[0-9]+)/$', views.data_detail),
    url(r'^user/$', views.user_data),
    url(r'^user/register/$', views.create_user),
]