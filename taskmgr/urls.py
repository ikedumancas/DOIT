from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'taskmgr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Auth URL
    url(r'^accounts/edit/$', 'account.views.auth_edit', name='account_edit'),
    url(r'^accounts/changepassword/$', 'account.views.auth_changepassword', name='auth_changepassword'),
    url(r'^accounts/login/$', 'account.views.auth_login', name='login'),
    url(r'^accounts/logout/$', 'account.views.auth_logout', name='logout'),
    url(r'^accounts/register/$', 'account.views.auth_register', name='register'),
    
    # List url
    url(r'^$', 'tasks.views.home', name='home'),
    url(r'^todolist/create/$', 'tasks.views.list_create', name='list_create'),
    url(r'^todolist/(?P<list_slug>[\w-]+)/deluser/(?P<id>\d+)/$', 'tasks.views.list_delete_user', name='list_delete_user'),
    url(r'^todolist/(?P<list_slug>[\w-]+)/edit/$', 'tasks.views.list_edit', name='list_edit'),
    url(r'^todolist/(?P<list_slug>[\w-]+)/archive/$', 'tasks.views.list_archive', name='list_archive'),
    url(r'^todolist/reaorder/$', 'tasks.views.todo_ajax_reorder', name='todo_ajax_reorder'),
    # Task url
    url(r'^todo/create/$', 'tasks.views.task_create', name='task_create'),
    url(r'^todo/(?P<task_slug>[\w-]+)/edit/$', 'tasks.views.task_edit', name='task_edit'),
    url(r'^todo/(?P<task_slug>[\w-]+)/done/$', 'tasks.views.task_done', name='task_done'),
    url(r'^todo/(?P<task_slug>[\w-]+)/undone/$', 'tasks.views.task_undone', name='task_undone'),
    url(r'^todo/(?P<task_slug>[\w-]+)/archive/$', 'tasks.views.task_archive', name='task_archive'),

    url(r'^notifications/$', 'notifications.views.all', name='notifications_all'),
    url(r'^notifications/read/all/$', 'notifications.views.read_all', name='notifications_read_all'),
    url(r'^notifications/read/(?P<id>\d+)/$', 'notifications.views.read', name='notifications_read'),

    url(r'^admin/', include(admin.site.urls)),
]
