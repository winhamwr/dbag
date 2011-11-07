
from django.contrib.auth.models import User

from dbag import dbag
from dbag.metric_types import MetricType, QueryMetric, String, QueryFilter

class UserMetric(QueryMetric):
    query_model = User

dbag.register_metric_type('users_metric', UserMetric)

class ActiveUsersCount(UserMetric):
    default_query_filter = {'key': 'is_active', 'value': True}

dbag.register_metric_type('active_users_count', ActiveUsersCount)
