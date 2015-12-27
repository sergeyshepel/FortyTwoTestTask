from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.hello.views',
    url(
        r'^$', 'index', name='index'
    ),
    url(
        r'^requests/$', 'requests', name='requests'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$', 'edit', name='edit'
    ),
    url(
        r'^team/$', 'add_team', name='add_team'
    ),
)
