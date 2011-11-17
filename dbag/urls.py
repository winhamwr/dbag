from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url('^$', 'dbag.views.index',
        name="dbag-index"),
    url('^metric/([\w-]+)/$', 'dbag.views.metric_detail',
        name="dbag-metric-detail"),
    url('^metric/([\w-]+).json$', 'dbag.views.metric_json',
        name="dbag-metric-json"),
)
