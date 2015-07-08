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
    
    # Tasks url
    url(r'^$', 'tasks.views.home', name='home'),
    url(r'^todolist/create$', 'tasks.views.list_create', name='list_create'),
    url(r'^todolist/reaorder/$', 'tasks.views.todo_ajax_reorder', name='todo_ajax_reorder'),
    url(r'^todo/create$', 'tasks.views.task_create', name='task_create'),
    url(r'^todo/edit/(?P<task_slug>[\w-]+)/$', 'tasks.views.task_edit', name='task_edit'),
    url(r'^todo/done/(?P<task_slug>[\w-]+)/$', 'tasks.views.task_done', name='task_done'),
    url(r'^todo/undone/(?P<task_slug>[\w-]+)/$', 'tasks.views.task_undone', name='task_undone'),
    url(r'^todo/archive/(?P<task_slug>[\w-]+)/$', 'tasks.views.task_archive', name='task_archive'),


    url(r'^admin/', include(admin.site.urls)),
]
