
from django.contrib.auth.models import User
from django.core import management
from django.test import TestCase

from dbag.models import DataSample, Metric, MetricManager
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
        self.dbag.register_metric_type('active_users_count', ActiveUsersCount)

    def test_builtin_registration(self):
        self.assertEqual(len(self.dbag.get_metric_types()), 2)

    def test_active_user_count_collect(self):
        # Ensure that gathering the active user account data actually counts
        # the number of active users
        slug = 'active_users_count'
        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug=slug,
            description='Total number of active user accounts')

        self.dbag.collect_metrics()

        active_users_count = Metric.objects.get(slug=slug)
        latest_sample = active_users_count.get_latest_sample()

        self.assertEqual(latest_sample.value, 1)

    def test_parameterized_metric(self):
        # Ensure that gathering the active user account data actually counts
        # the number of active users
        slug = 'staff_users'
        self.dbag.create_metric(
            metric_type_label='users_metric',
            label='Number of Staff Users',
            slug=slug,
            description='Total number of active staff user accounts',
            query_filter={'key': 'is_staff', 'value': True},
        )

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

class CommandsTest(TestCase):
    """
    Test the management commands
    """

    def setUp(self):
        self.dbag = MetricManager()
        self.dbag.register_metric_type('users_metric', UserMetric)
        self.dbag.register_metric_type('active_users_count', ActiveUsersCount)

    def test_collect_metrics(self):
        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug='active_user_count1',
            description='Total number of active user accounts')
        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug='active_user_count2',
            description='Total number of active user accounts')
        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug='active_user_count3',
            description='Total number of active user accounts',
            do_collect=False,
        )

        self.assertEqual(DataSample.objects.count(), 0)

        management.call_command('dbag_collect_metrics')

        # The two metrics were gathered once and the disabled metric wasn't
        # gathered
        self.assertEqual(DataSample.objects.count(), 2)


