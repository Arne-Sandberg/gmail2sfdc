from django.conf.urls import patterns, url
from accounts import views


urlpatterns = patterns('',
                       url(r'^google-login$', views.google_login, name='google_login'),
                       url(r'^gmail-oauth$', views.gmail_oauth, name='gmail_oauth'),
                       url(r'^googleAuthCallback$', views.google_oauth_callback, name='google_oauth_callback'),
                       url(r'^sfdc-oauth', views.sfdc_oauth, name='sfdc_oauth'),
                       url(r'^sfdcAuthCallback$', views.sfdc_oauth_callback, name='sfdc_oauth_callback'),
                       url(r'^logout', views.logout, name='google_login'),
)