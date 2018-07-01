from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from hello_word import settings
import word.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'hello_word.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', word.views.index, name='index'),
    url(r'^word/$', word.views.word, name='word'),
    url(r'^learn/$', word.views.learn, name='learn'),
    url(r'^progress/$', word.views.progress, name='progress'),
    url(r'^review/$', word.views.review, name='review'),
    url(r'^test/$', word.views.test, name='test'),
    url(r'^test_entry/$', word.views.test_entry, name='test_entry'),
    url(r'^wordsets/$', word.views.wordsets, name='wordsets'),
    url(r'^mywords/$', word.views.mywords, name='mywords'),
    url(r'^word_per_day/$',word.views.word_per_day, name='word_per_day'),
    
    url(r'^login/$', word.views.my_login, name='login'),
    url(r'^signup/$', word.views.my_signup, name='signup'),
    url(r'^logout/$', word.views.my_logout, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),

    url(r'^api/get_a_master_word/$',word.views.get_a_master_word, name='get_a_master_word'),

    url(r'^api/get_a_word/$',word.views.get_a_word, name='get_a_word'),
    url(r'^api/unknow/$',word.views.unknow, name='unknow'),
    url(r'^api/star/$',word.views.star, name='star'),

    url(r'^api/choose/$',word.views.choose, name='choose'),
    url(r'^api/set_wordset/$',word.views.set_wordset, name='set_wordset'),

]
