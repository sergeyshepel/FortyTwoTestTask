from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.hello.views',
    url(
        r'^$', 'index', name='index'
    ),
    url(
        r'^requests/$', 'requests', name='requests'
    ),
)
