import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

CRON_TPL = ''' # Minute    Hour    DoM     Month   DoW
# Start metric collection at 12:01am and pip the output stdout and stderr to a log file
01          00      *       *       *   <my_user> cd /path/to/project && /path/to/python manage.py dbag_collect_metrics >> /path/to/log/file.log 2>&1
# Newline placeholder for sanity
'''
class Command(BaseCommand):
    args = ''
    help = 'Generate a template cron file for collecting daily dbag metrics'

    def handle(self, *args, **kwargs):
        print CRON_TPL

