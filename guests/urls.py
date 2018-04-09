from django.conf.urls import url
from django.contrib.auth import views as auth_views

from guests.views import GuestListView, export_guests, \
    invitation, rsvp_confirm, dashboard, rsvp_redirect

urlpatterns = [
    # url(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    # url(r'^guests/export$', export_guests, name='export-guest-list'),
    url(r'^rsvp/invite/(?P<invite_id>[\w-]+)/$', invitation, name='invitation'),
    url(r'^rsvp/confirm/(?P<invite_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
    url(r'^rsvp/$', auth_views.login,{'template_name': 'guests/login.html'}, name='rsvp-login'),
    url(r'^rsvp-logout/$', auth_views.logout, name='rsvp-logout'),

    url(r'^rsvp/redirect/$', rsvp_redirect, name='rsvp-redirect'),

]
