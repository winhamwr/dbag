
from django.contrib.auth.models import User

from dbag import dbag
from dbag.metric_types import MetricType, QueryMetric, String, QueryFilter

class ActiveUsersCount(QueryMetric):
    query_model = User
    query_filter = {'key': 'is_active', 'value': True}
    user_filter = QueryFilter()

    def filter_results(self, query):
        if user_filter:
            return query.filter(
                **{user_filter.key: user_filter.value})
        return query

dbag.register('active_users_count', ActiveUsersCount)
