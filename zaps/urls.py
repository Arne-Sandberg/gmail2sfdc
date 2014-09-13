from django.conf.urls import patterns, url
from zaps import views


urlpatterns = patterns('',
                       url(r'^$', views.connect_apps, name='connect_apps'),
                       url(r'^emails', views.emails, name='emails'),
                       url(r'^list', views.list_threads, name='list_threads'),
                       url(r'^sfupload', views.upload_to_sfdc, name='upload_to_sfdc'),
)