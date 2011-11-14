import logging

from django.core import management
from django.core.management.base import BaseCommand

from dbag import autodiscover

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''
    help = 'Collect data samples for all Metrics with collection enabled'

    def handle(self, *args, **kwargs):
        autodiscover()

        logger.info("Loading initial dbag metrics")
        management.call_command(
            'loaddata', 'dbag_initial_metrics.json', verbosity=0, interactive=False)
