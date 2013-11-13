from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'lunch_economy.apps.core.views.home', name='home'),

    url(r'^login/$', 'lunch_economy.apps.users.views.log_in', name='login'),
    url(r'^logout/$', 'lunch_economy.apps.users.views.log_out', name='logout'),

    url(r'^user/(?P<user_id>\d+)/', 'lunch_economy.apps.users.views.user_detail', name='user_detail'),
    url(r'^user/me/', 'lunch_economy.apps.users.views.me', name='me'),

    url(r'^mail/inbox/', 'lunch_economy.apps.mail.views.inbox', name='inbox'),
    url(r'^mail/(?P<mail_id>\d+)/', 'lunch_economy.apps.mail.views.mail_detail', name='mail_detail'),

    url(r'^groups/$', 'lunch_economy.apps.groups.views.my_groups', name='my_groups'),
    url(r'^groups/(?P<group_id>\d+)/$', 'lunch_economy.apps.groups.views.group_detail', name='group_detail'),
    url(r'^groups/create/$', 'lunch_economy.apps.groups.views.create_group', name='create_group'),
    url(r'^groups/join/$', 'lunch_economy.apps.groups.views.join_group', name='join_group'),
    url(r'^groups/request/send/(?P<group_id>\d+)/$', 'lunch_economy.apps.groups.views.send_request', name='send_request'),
    url(r'^groups/request/approve/(?P<group_id>\d+)/(?P<user_id>\d+)/$', 'lunch_economy.apps.groups.views.approve_request', name='approve_request'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
