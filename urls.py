from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^articles/$', 'blogproject.articles.views.index'),
    url(r'^articles/details/(?P<slug>[^\.]+)/',
        'blogproject.articles.views.article_details', name='article_details'),
    url(r'^articles/add/$', 'blogproject.articles.views.add'),
    url(r'^articles/edit/(?P<article_id>\d+)/$', 'blogproject.articles.views.edit'),
    url(r'^articles/delete/(?P<article_id>\d+)/$', 'blogproject.articles.views.delete'),                       

    url(r'^comments/add/$', 'blogproject.articles.views.add_comment'),
    url(r'^comments/delete/(?P<comment_id>\d+)/$',
        'blogproject.articles.views.delete_comment'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/profile/$', 'blogproject.userprofile.views.profile'),                       
                           
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
