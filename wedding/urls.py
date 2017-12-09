from django.conf.urls import url

from wedding import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
