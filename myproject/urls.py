from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import home

urlpatterns = [
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^kaizing/', include('kaizing.urls',namespace="kaizing")),
    url(r'^$',home),
]
