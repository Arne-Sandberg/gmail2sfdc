from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'gmail2sfdc.views.home', name='home'),
                       url(r'^close$', 'gmail2sfdc.views.close_window', name='close_window'),
                       url(r'^auth/', include('accounts.urls')),
                       url(r'^zap/', include('zaps.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
