"""
Dbag- Easy time-series metrics and dashboarding
"""
import copy

__version__ = '0.1.2'
__author__ = 'Wes Winham'
__contact__ = 'winhamwr@gmail.com'
__homepage__ = 'http://github.com/winhamwr/dbag'

__all__ = ('dbag_manager', 'autodiscover')

from dbag.manager import dbag_manager

def autodiscover():
    """
    Auto-discover all ``MetricTypes`` inside ``dbag_metric_types`` modules on
    all ``INSTALLED_APPS``.
    """
    from django.conf import settings
    from django.utils.importlib import import_module

    for app in settings.INSTALLED_APPS:
        # Attempt to import the dbag_metric_types module
        before_import_registry = copy.copy(dbag_manager._registry)
        try:
            module_name = '%s.dbag_metric_types' % app
            import_module(module_name)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            dbag_manager._registry = before_import_registry

