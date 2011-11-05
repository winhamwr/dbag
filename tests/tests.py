
from django.contrib.auth.models import User
from django.test import TestCase

from dbag import create_metric, collect_metrics
from dbag.models import Metric, Datum

class ContribMetricsTest(TestCase):
    """
    Tests on the correctness of the built-in ``MetricTypes``.
    """
    urls = 'tests.test_urls'

    def setUp(self):
        self.user = User.objects.create(username='admin', email='admin@example.com')

    def test_active_user_count_gather(self):
        # Ensure that gathering the active user account data actually counts
        # the number of active users
        create_metric(
            metric_type='active_user_count',
            label='Number of Active User Accounts',
            slug='active_user_count',
            description='Total number of active user accounts')

        collect_metrics()
