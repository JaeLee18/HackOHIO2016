from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.login, name='login' ),
    url(r'^register/$', views.register, name='register'),
    url(r'^password-reset/$',views.pw_reset,
		name='password_reset'),
    url(r'^makeGroup/$',views.makeGroup, name='makeGroup'),
    url(r'^group/$', views.GroupView, name = 'GroupView'),
    url(r'^JoinGroup/$', views.JoinGroup, name = 'JoinGroup'),
    url(r'^bankConnect/$', views.ConnectBank, name = 'bankConnect'),
    url(r'^transfer/$', views.transfer, name = 'transfer'),
    url(r'^home/$', views.check, name = 'check'),
    url(r'^confirm/$', views.confirm, name= 'confirm')
]