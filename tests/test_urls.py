
from django.conf.urls.defaults import patterns, include

import dbag
dbag.autodiscover()

urlpatterns = patterns('',
   (r'^dbag/', include('dbag.urls')),
)

