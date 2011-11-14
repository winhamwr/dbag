import logging

from django.core.management.base import BaseCommand

from dbag import autodiscover, dbag_manager
from dbag.models import Metric

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Collect data samples for all Metrics with collection enabled'

    def handle(self, *args, **kwargs):
        autodiscover()

        num_metrics = Metric.objects.filter(do_collect=True).count()
        logger.info("Collecting data samples for %s Metrics", num_metrics)

        data_samples = dbag_manager.collect_metrics()

        logger.info("Collected %s data samples", len(data_samples))

