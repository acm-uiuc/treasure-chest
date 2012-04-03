from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('treasureapp.views',
    # Treasureapp URLs
    url(r'^/account/(?P<account_id>\d+)$', 'account_detail'),
    url(r'^/account/$', 'accounts'),
    url(r'^$', 'index'),
)

urlpatterns += patterns('',
    # Administration controls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
