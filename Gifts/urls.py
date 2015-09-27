# example/simple/urls.py

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^recommendations/(\w*)', views.recommendations, name='recommendations'),
    # url(r'^login/(\w*)', views.login, name='login')
)