
import datetime
import logging
from random import normalvariate

from django.core.management.base import BaseCommand

from dbag import autodiscover, dbag_manager
from dbag.models import Metric, DataSample

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Fake 60 days worth of data for all metrics'

    def handle(self, *args, **kwargs):
        autodiscover()

        metrics = Metric.objects.filter(do_collect=True)
        logger.info("Faking 60 days of data samples for %s Metrics", metrics.count())

        for metric in metrics:
            self._get_samples_for_metric(dbag_manager, metric)

    def _get_samples_for_metric(self, manager, metric):
        """
        Get 60 days worth of samples going back in time for the given metric.
        """
        utc_now = datetime.datetime.utcnow()
        one_day = datetime.timedelta(days=1)
        start_day = utc_now - datetime.timedelta(days=60)

        previous_sample = None
        day_counter = utc_now
        while day_counter > start_day:
            previous_sample = self._fake_sample(manager, metric, day_counter, previous_sample)
            day_counter = day_counter - one_day

    def _fake_sample(self, manager, metric, utc_timestamp, seed_sample):
        """
        If a sample for the given day doesn't exist, fake it.
        """
        existing_sample = metric.get_sample_for_day(utc_timestamp)

        if existing_sample:
            return existing_sample

        if seed_sample is None:
            # Let's try collecting an actual sample to give our data some meaning
            return metric.collect_data_sample(manager)

        new_value = normalvariate(seed_sample.value, 1)
        return DataSample.objects.create(
            metric=metric, utc_timestamp=utc_timestamp, value=new_value)
