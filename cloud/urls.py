from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import (base, login_view, signup, logout_view, profile, show_output, docker_list, docker_launch, docker_manage, docker_start,docker_stop,docker_shell,docker_remove,choose)
# import docker_stop

urlpatterns = [
	url(r'^$', base, name='base'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view,  name='logout'),
	url(r'^signup/$', signup, name='signup'),
	url(r'^choose/$', choose, name='choose'),
	url(r'^show-output/$', show_output,name='show'),
	url(r'^profile/$', profile, name='profile'),
	url(r'^images/$', docker_list, name='images'),
	url(r'^img-cont/$', docker_launch, name='img-cont'),
	url(r'^dock-manage/$', docker_manage, name='dock-manage'),
	url(r'^dock-manage/docker_start/(?P<mycname>[\w|\W]+)/$', docker_start, name='dock-start'),
	url(r'^dock-manage/docker_stop/(?P<mycname>[\w|\W]+)/$', docker_stop, name='dock-stop'),
	url(r'^dock-manage/docker_shell/(?P<mycname>[\w|\W]+)/$', docker_shell, name='dock-shell'),
	url(r'^dock-manage/docker_remove/(?P<mycname>[\w|\W]+)/$', docker_remove, name='dock-remove')
]
