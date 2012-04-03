from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('treasureapp.views',
    # Treasureapp URLs
    url(r'^/account/(?P<account_id>\d+)$', 'account_detail', {}, 'account_detail'),
    url(r'^/account/$', 'accounts', {}, 'account_list'),
    url(r'^$', 'index', {}, 'index'),
)

urlpatterns += patterns('',
    # Administration controls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG == True:
    urlpatterns += patterns('',
        # Static files (development server only)
        (r'^assets/(?P<path>.*)', 'django.views.static.serve',
            { 'document_root' : settings.ASSETS_ROOT })
    )
