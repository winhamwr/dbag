
from django.conf import settings
from django.contrib.auth.models import User
from django.core import management
from django.test import TestCase
from django.test.client import Client

from dbag.manager import MetricManager
from dbag.models import DataSample, Metric
from dbag.dbag_metric_types import UserMetric, ActiveUsersCount

class ContribMetricsTest(TestCase):
    """
    Tests on the correctness of the built-in ``MetricTypes``.
    """

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

    def test_fake_metrics(self):
        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug='active_user_count1',
            description='Total number of active user accounts')
        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug='active_user_count2',
            description='Total number of active user accounts',
        )

        self.assertEqual(DataSample.objects.count(), 0)

        management.call_command('dbag_fake_metrics')

        # We should get 60 days worth of data times 2
        self.assertEqual(DataSample.objects.count(), 2*60)

        # Running the command again won't double up on the data
        management.call_command('dbag_fake_metrics')
        self.assertEqual(DataSample.objects.count(), 2*60)


class ClientTests(TestCase):
    """
    Test the views.
    """
    urls = 'tests.test_urls'

    def setUp(self):
        self.dbag = MetricManager()
        self.dbag.register_metric_type('users_metric', UserMetric)
        self.dbag.register_metric_type('active_users_count', ActiveUsersCount)

        self.dbag.create_metric(
            metric_type_label='active_users_count',
            label='Number of Active User Accounts',
            slug='active_user_count',
            description='Total number of active user accounts')
        self.dbag.create_metric(
            metric_type_label='users_metric',
            label='Number of User Accounts',
            slug='user_accounts',
            description='Total number of user accounts',
        )

        self.client = Client()

    def test_no_metrics_collected_index(self):
        # When a metric has no data yet, we shouldn't crash
        response = self.client.get('/dbag/')

        self.assertContains(response, 'Number of Active User Accounts')
        self.assertContains(response, 'Number of User Accounts')
        # One for each metric and one if the first collected metric (the oldest)
        # has no data
        self.assertContains(response, 'class="no-data-collected"', 2 + 1)
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)

    def test_zero_values_display(self):
        # Shouldn't confuse a zero value with no data
        management.call_command('dbag_collect_metrics')

        # All values are zero
        for ds in DataSample.objects.all():
            self.assertEqual(ds.value, 0)

        response = self.client.get('/dbag/')

        self.assertContains(response, 'Number of Active User Accounts')
        self.assertContains(response, 'Number of User Accounts')
        self.assertNotContains(response, 'class="no-data-collected"')
        self.assertNotContains(response, settings.TEMPLATE_STRING_IF_INVALID)
