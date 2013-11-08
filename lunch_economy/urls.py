from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lunch_economy.apps.core.views.home', name='home'),
    url(r'^login$', 'lunch_economy.apps.core.views.log_in', name='login'),
    url(r'^logout$', 'lunch_economy.apps.core.views.log_out', name='logout'),
    # url(r'^lunch_economy/', include('lunch_economy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
