
from django.conf.urls.defaults import patterns, url

import dbag
dbag.autodiscover()

urlpatterns = patterns(''
   url('^dbag/', include('dbag.urls'),
)

