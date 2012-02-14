from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'treasure_chest.views.home', name='home'),
    # url(r'^treasure_chest/', include('treasure_chest.foo.urls')),

    # Administration controls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
