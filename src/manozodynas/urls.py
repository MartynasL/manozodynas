from django.conf.urls import patterns, url
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from twisted.trial.util import _WorkingDirectoryBusy

from .views import index_view, login_view, wordlist_view, AddWordView,\
    translationlist_view

urlpatterns = patterns('',
                       url(r'^$', index_view, name='index'),
                       url(r'^login$', login_view, name='login'),
                       url(r'^wordlist$', wordlist_view, name='word_list'),
                       url(r'^addword$', AddWordView.as_view() , name='add_word'),
                       url(r'^translationlist$', translationlist_view , name='add_word'),
                       )

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}),
                        )
