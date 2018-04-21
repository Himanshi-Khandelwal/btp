from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import (base, login_view, signup, logout_view, code_platform,
		show_output, docker_list, docker_launch, docker_manage, docker_start,
		docker_stop,ubuntu_shell,centos_shell,docker_remove,choose, terminal,simple_upload,
		download_file)
# import docker_stop

urlpatterns = [
	url(r'^$', base, name='base'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view,  name='logout'),
	url(r'^signup/$', signup, name='signup'),
	url(r'^choose/$', choose, name='choose'),
	url(r'^show-output/$', show_output,name='show'),
	url(r'^code-platform/$', code_platform, name='code-platform'),
	url(r'^images/$', docker_list, name='images'),
	url(r'^img-cont/$', docker_launch, name='img-cont'),
	url(r'^terminal/$', terminal, name='terminal'),
	url(r'^dock-manage/$', docker_manage, name='dock-manage'),
	url(r'^dock-manage/docker_start/(?P<mycname>[\w|\W]+)/$', docker_start, name='dock-start'),
	url(r'^dock-manage/docker_stop/(?P<mycname>[\w|\W]+)/$', docker_stop, name='dock-stop'),
	url(r'^ubuntu-shell/$', ubuntu_shell, name='ubuntu-shell'),
	url(r'^centos-shell/$', centos_shell, name='centos-shell'),
	url(r'^dock-manage/docker_remove/(?P<mycname>[\w|\W]+)/$', docker_remove, name='dock-remove'),
	url(r'^toconvert/$', simple_upload, name='conversion'),
	url(r'^downloads/(?P<fname>[\w|\W]+)/$', download_file, name='downloads'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
