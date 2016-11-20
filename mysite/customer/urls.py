from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.login, name='login' ),
    url(r'^register/$', views.register, name='register'),
    url(r'^password-reset/$',views.pw_reset,
		name='password_reset'),
    url(r'^makeGroup/$',views.makeGroup, name='makeGroup'),
]