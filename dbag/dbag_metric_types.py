
from django.contrib.auth.models import User

from dbag import dbag_manager
from dbag.metric_types import QueryMetric

class UserMetric(QueryMetric):
    query_model = User

dbag_manager.register_metric_type('users_metric', UserMetric)

class ActiveUsersCount(UserMetric):
    default_query_filter = {'key': 'is_active', 'value': True}

dbag_manager.register_metric_type('active_users_count', ActiveUsersCount)
