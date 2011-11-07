
from django.contrib.auth.models import User
from django.test import TestCase

from dbag.models import Metric, DatumSample, MetricManager
from dbag.dbag_metric_types import UserMetric, ActiveUsersCount

class ContribMetricsTest(TestCase):
    """
    Tests on the correctness of the built-in ``MetricTypes``.
    """
    urls = 'tests.test_urls'

    def setUp(self):
        self.user = User.objects.create(username='admin', email='admin@example.com')
        self.dbag = MetricManager()
        self.dbag.register_metric_type('users_metric', UserMetric)
        self.dbag.register_metric_type('active_user_count', ActiveUsersCount)

    def test_builtin_registration(self):
        self.assertEqual(len(self.dbag.get_metric_types()), 2)

    def test_active_user_count_gather(self):
        # Ensure that gathering the active user account data actually counts
        # the number of active users
        slug = 'active_user_count'
        self.dbag.create_metric(
            metric_type_label='active_user_count',
            label='Number of Active User Accounts',
            slug=slug,
            description='Total number of active user accounts')

        self.dbag.collect_metrics()

        active_user_count = Metric.objects.get(slug=slug)
        latest_sample = active_user_count.get_latest_sample()

        self.assertEqual(latest_sample.value, 1)

    def test_parameterized_metric(self):
        # Ensure that gathering the active user account data actually counts
        # the number of active users
        slug = 'staff_users'
        m = self.dbag.create_metric(
            metric_type_label='users_metric',
            label='Number of Staff Users',
            slug=slug,
            description='Total number of active user accounts',
            query_filter={'key': 'is_staff', 'value': True},
        )
        print m.metric_properties

        self.dbag.collect_metrics()

        staff_user_count = Metric.objects.get(slug=slug)
        latest_sample = staff_user_count.get_latest_sample()

        self.assertEqual(latest_sample.value, 0)

        # Make the user a staff user and ensure the next metric collection
        # reflects that
        self.user.is_staff = True
        self.user.save()

        self.dbag.collect_metrics()
        latest_sample = staff_user_count.get_latest_sample()

        self.assertEqual(latest_sample.value, 1)

