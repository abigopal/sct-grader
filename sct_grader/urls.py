from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grader/', include('grader.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^/register/', include('grader.views.auth.register'), name='register'),
    # Examples:
    # url(r'^$', 'sct_grader.views.home', name='home'),
    # url(r'^sct_grader/', include('sct_grader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
