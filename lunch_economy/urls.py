from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lunch_economy.apps.core.views.home', name='home'),
    url(r'^login/$', 'lunch_economy.apps.core.views.log_in', name='login'),
    url(r'^logout/$', 'lunch_economy.apps.core.views.log_out', name='logout'),

    url(r'^mail/inbox/', 'lunch_economy.apps.mail.views.inbox', name='inbox'),
    url(r'^mail/(?P<mail_id>\d+)/', 'lunch_economy.apps.mail.views.mail_detail', name='mail_detail'),

    url(r'^mygroups/$', 'lunch_economy.apps.groups.views.my_groups', name='my_groups'),
    url(r'^mygroups/create/$', 'lunch_economy.apps.groups.views.create_group', name='create_group'),
    url(r'^mygroups/(?P<group_id>\d+)/$', 'lunch_economy.apps.groups.views.group_detail', name='group_detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
