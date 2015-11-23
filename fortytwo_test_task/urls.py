from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(
        r'^', include('apps.hello.urls')
    ),
    url(
        r'^admin/', include(admin.site.urls)
    ),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name': 'hello/index.html'},
        name='login',
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='logout'
    ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
