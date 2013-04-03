from django.conf.urls import url, patterns

urlpatterns = patterns('syntaxhighlighter.views',
    url(r'^$', 'highlight', name='highlighter'),
)
